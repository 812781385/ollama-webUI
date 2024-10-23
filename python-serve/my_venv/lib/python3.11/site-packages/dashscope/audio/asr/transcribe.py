import asyncio
import os
from http import HTTPStatus
from typing import Any, Dict
from urllib.parse import urlparse

import aiohttp

from dashscope.api_entities.dashscope_response import DashScopeAPIResponse
from dashscope.client.base_api import BaseApi
from dashscope.common.constants import ApiProtocol, HTTPMethod
from dashscope.common.error import InputRequired
from dashscope.common.utils import _get_task_group_and_task


class Transcribe(BaseApi):
    """API for File Transcriber models.

    """

    MAX_QUERY_TRY_COUNT = 3

    @classmethod
    def call(cls, model: str, file: str, **kwargs) -> DashScopeAPIResponse:
        """Call file transcriber model service.

        Args:
            model (str): The requested model, such as paraformer-16k-1
            file (str): The local path or URL of the file.
            channel_id (List[int], optional): The selected channel_id of audio file. # noqa: E501

        Returns:
            DashScopeAPIResponse: The response body.

        Raises:
            InputRequired: The file cannot be empty.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(cls.async_call(model, file, **kwargs))

    @classmethod
    async def async_call(cls, model: str, file: str,
                         **kwargs) -> DashScopeAPIResponse:
        """Async call file transcriber model service.

        Args:
            model (str): The requested model, such as paraformer-16k-1
            file (str): The local path or URL of the file.
            channel_id (List[int], optional): The selected channel_id of audio file. # noqa: E501

        Returns:
            DashScopeAPIResponse: The response body.

        Raises:
            InputRequired: The file cannot be empty.
        """
        cls.is_url = cls._validate_file(file)
        cls.file_name = file
        cls.model_id = model

        request = {'file': cls.file_name, 'is_url': cls.is_url}

        # launch transcribe request, and get task info.
        task = await cls._async_launch_requests(request, **kwargs)

        response = await cls._async_get_result(task, **kwargs)

        return response

    @classmethod
    async def _async_launch_requests(cls, request: Dict[str, Any], **kwargs):
        """Async submit transcribe request.

        Args:
            inputs (Dict[str, Any]): The input parameters.

        Returns:
            task (Dict[str, Any]): The result of the task request.
        """
        inputs = {'file_link': request['file']}
        task = {'file': request['file']}
        local_file = None
        try_count: int = 0
        response = DashScopeAPIResponse(id='', code=HTTPStatus.OK, output=None)
        if not request['is_url']:
            try:
                local_file = open(inputs['file_link'], 'rb')
            except IOError as e:
                raise InputRequired(f'File cannot be opened. {e}')

            kwargs['form'] = {'av_file': local_file}

        task_name, function = _get_task_group_and_task(__name__)
        kwargs['async_request'] = True
        kwargs['query'] = False

        while True:
            try:
                response = await super().async_call(
                    model=cls.model_id,
                    task_group='audio',
                    task=task_name,
                    function=function,
                    input=inputs,
                    api_protocol=ApiProtocol.HTTP,
                    http_method=HTTPMethod.POST,
                    **kwargs)

                task['request_id'] = response.id
                task['code'] = response.code
                task['status'] = response.status

                if response.code == HTTPStatus.OK and response.output is not None:  # noqa: E501
                    task.update(response.output)
                else:
                    task['message'] = response.message

                break

            except (asyncio.TimeoutError, aiohttp.ClientConnectorError) as e:
                try_count += 1
                if try_count > Transcribe.MAX_QUERY_TRY_COUNT:
                    task['request_id'] = response.id
                    task['code'] = HTTPStatus.REQUEST_TIMEOUT
                    task['status'] = response.status
                    task['message'] = str(e)
                    break
                else:
                    await asyncio.sleep(2)
                    continue
            except Exception as e:
                task['request_id'] = response.id
                task['code'] = HTTPStatus.BAD_REQUEST
                task['status'] = response.status
                task['message'] = str(e)
                break

        if local_file is not None:
            local_file.close()

        return task

    @classmethod
    async def _async_get_result(cls, task, **kwargs):
        """Async get transcribe result by polling.

        Args:
            task (Dict[str, Any]): The info of the task request.

        Returns:
            DashScopeAPIResponse: The response body.
        """
        request = task
        responses = []
        item = {}
        response = DashScopeAPIResponse(id=request['request_id'],
                                        code=request['code'],
                                        output=None,
                                        status=request['status'],
                                        message=request['message'])

        if request['code'] != HTTPStatus.OK:
            item['file'] = request['file']
            item['request_id'] = response.id
            item['code'] = request['code']
            item['status'] = request['status']
            item['message'] = request['message']
            responses.append(item)
        else:
            try_count: int = 0
            while True:
                item['file'] = request['file']
                item['task_Id'] = request['task_id']

                try:
                    inputs = {}
                    inputs['task_Id'] = request['task_id']
                    kwargs['async_request'] = True
                    kwargs['query'] = True

                    response = await super().async_call(
                        model=cls.model_id,
                        task_group=None,
                        task='tasks',
                        input=inputs,
                        task_id=inputs['task_Id'],
                        api_protocol=ApiProtocol.HTTP,
                        http_method=HTTPMethod.GET,
                        **kwargs)
                except (asyncio.TimeoutError,
                        aiohttp.ClientConnectorError) as e:
                    try_count += 1
                    if try_count > Transcribe.MAX_QUERY_TRY_COUNT:
                        item['request_id'] = response.id
                        item['code'] = HTTPStatus.REQUEST_TIMEOUT
                        item['status'] = response.status
                        item['message'] = str(e)
                        responses.append(item)
                        break
                    else:
                        await asyncio.sleep(2)
                        continue
                except Exception as e:
                    item['request_id'] = response.id
                    item['code'] = HTTPStatus.BAD_REQUEST
                    item['status'] = response.status
                    item['message'] = str(e)
                    responses.append(item)
                    break

                try_count = 0
                item['request_id'] = response.id
                item['code'] = response.code
                item['status'] = response.status

                if response.code == HTTPStatus.OK:
                    if 'task_status' in response.output:
                        task_status = response.output['task_status']
                        if task_status == 'QUEUING' or task_status == 'PROCESSING':  # noqa: E501
                            await asyncio.sleep(2)
                            continue

                    item.update(response.output)
                else:
                    item['message'] = response.message

                responses.append(item)
                break

        output = {}
        output['results'] = responses

        return DashScopeAPIResponse(id=response.id,
                                    code=response.code,
                                    status=response.status,
                                    message=response.message,
                                    output=output)

    @classmethod
    def _validate_file(cls, file: str):
        """Check the validity of the file
        and whether the file is a URL or a local path.

        Args:
            file (str): The local path or URL of the file.

        Returns:
            bool: Whether the file is a URL.
        """
        if file is None or len(file) == 0:
            raise InputRequired(
                'Input an illegal file, please ensure that the file type is a local path or URL!'  # noqa: *
            )

        if os.path.isfile(file):
            return False
        else:
            result = urlparse(file)
            if result.scheme is not None and len(result.scheme) > 0:
                if result.scheme != 'http' and result.scheme != 'https':
                    raise InputRequired(
                        f'The URL protocol({result.scheme}) of file({file}) is not http or https.'  # noqa: *
                    )
            else:
                raise InputRequired(
                    f'Input an illegal file({file}), maybe the file is inexistent.'  # noqa: *
                )

        return True
