from typing import Union

from dashscope.api_entities.dashscope_response import DashScopeAPIResponse
from dashscope.client.base_api import (CancelMixin, CreateMixin, DeleteMixin,
                                       GetStatusMixin, ListMixin, LogMixin,
                                       StreamEventMixin)


class FineTune(CreateMixin, CancelMixin, DeleteMixin, ListMixin,
               GetStatusMixin, StreamEventMixin, LogMixin):
    SUB_PATH = 'fine-tunes'

    @classmethod
    def call(cls,
             model: str,
             training_file_ids: Union[list, str],
             validation_file_ids: Union[list, str] = None,
             mode: str = None,
             hyper_parameters: dict = {},
             api_key: str = None,
             workspace: str = None,
             **kwargs) -> DashScopeAPIResponse:
        """Create fine-tune job

        Args:
            model (str): The model to be fine-tuned
            training_file_ids (list, str): Ids of the fine-tune training data,
                which can be pre-uploaded using the File API.
            validation_file_ids ([list,str], optional): Ids of the fine-tune
                validating data, which can be pre-uploaded using the File API.
            mode (str): The fine-tune mode, sft or efficient_sft.
            hyper_parameters (dict, optional): The fine-tune hyper parameters.
                Defaults to empty.
            api_key (str, optional): The api key. Defaults to None.
            workspace (str): The dashscope workspace id.

        Returns:
            DashScopeAPIResponse: The request result.
        """
        request = {
            'model': model,
            'training_file_ids': training_file_ids,
            'validation_file_ids': validation_file_ids,
            'hyper_parameters': hyper_parameters if hyper_parameters else {},
        }
        if mode is not None:
            request['training_type'] = mode
        if 'finetuned_output' in kwargs:
            request['finetuned_output'] = kwargs['finetuned_output']
        return super().call(request,
                            api_key=api_key,
                            workspace=workspace,
                            **kwargs)

    @classmethod
    def cancel(cls,
               job_id: str,
               api_key: str = None,
               workspace: str = None,
               **kwargs) -> DashScopeAPIResponse:
        """Cancel a running fine-tune job.

        Args:
            job_id (str): The fine-tune job id.
            api_key (str, optional): The api api_key, can be None,
                if None, will get by default rule(TODO: api key doc).
            workspace (str): The dashscope workspace id.

        Returns:
            DashScopeAPIResponse: The request result.
        """
        return super().cancel(job_id, api_key, workspace=workspace, **kwargs)

    @classmethod
    def list(cls,
             page=1,
             page_size=10,
             api_key: str = None,
             workspace: str = None,
             **kwargs) -> DashScopeAPIResponse:
        """List fine-tune job.

        Args:
            api_key (str, optional): The api key
            page (int, optional): Page number. Defaults to 1.
            page_size (int, optional): Items per page. Defaults to 10.
            workspace (str): The dashscope workspace id.

        Returns:
            DashScopeAPIResponse: The fine-tune jobs in the result.
        """
        return super().list(page,
                            page_size,
                            api_key,
                            workspace=workspace,
                            **kwargs)

    @classmethod
    def get(cls,
            job_id: str,
            api_key: str = None,
            workspace: str = None,
            **kwargs) -> DashScopeAPIResponse:
        """Get fine-tune job information.

        Args:
            job_id (str): The fine-tune job id
            api_key (str, optional): The api key. Defaults to None.
            workspace (str): The dashscope workspace id.

        Returns:
            DashScopeAPIResponse: The job info
        """
        return super().get(job_id, api_key, workspace=workspace, **kwargs)

    @classmethod
    def delete(cls,
               job_id: str,
               api_key: str = None,
               workspace: str = None,
               **kwargs) -> DashScopeAPIResponse:
        """Delete a fine-tune job.

        Args:
            job_id (str): The fine-tune job id.
            api_key (str, optional): The api key. Defaults to None.
            workspace (str): The dashscope workspace id.

        Returns:
            DashScopeAPIResponse: The delete result.
        """
        return super().delete(job_id, api_key, workspace=workspace, **kwargs)

    @classmethod
    def stream_events(cls,
                      job_id: str,
                      api_key: str = None,
                      workspace: str = None,
                      **kwargs) -> DashScopeAPIResponse:
        """Get fine-tune job events.

        Args:
            job_id (str): The fine-tune job id
            api_key (str, optional): the api key. Defaults to None.
            workspace (str): The dashscope workspace id.

        Returns:
            DashScopeAPIResponse: The job log events.
        """
        return super().stream_events(job_id,
                                     api_key,
                                     workspace=workspace,
                                     **kwargs)

    @classmethod
    def logs(cls,
             job_id: str,
             offset=1,
             line=1000,
             api_key: str = None,
             workspace: str = None,
             **kwargs) -> DashScopeAPIResponse:
        """Get log of the job.

        Args:
            job_id (str): The job id(used for fine-tune)
            offset (int, optional): start log line. Defaults to 1.
            line (int, optional): total line return. Defaults to 1000.
            api_key (str, optional): The api key. Defaults to None.
            workspace (str): The dashscope workspace id.

        Returns:
            DashScopeAPIResponse: The response
        """
        return super().logs(job_id, offset, line, workspace=workspace)
