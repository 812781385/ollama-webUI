from typing import Dict, List, Optional

from dashscope.assistants.assistant_types import (Assistant, AssistantList,
                                                  DeleteResponse)
from dashscope.client.base_api import (CancelMixin, CreateMixin, DeleteMixin,
                                       GetStatusMixin, ListObjectMixin,
                                       UpdateMixin)
from dashscope.common.error import ModelRequired

__all__ = ['Assistants']


class Assistants(CreateMixin, CancelMixin, DeleteMixin, ListObjectMixin,
                 GetStatusMixin, UpdateMixin):
    SUB_PATH = 'assistants'

    @classmethod
    def _create_assistant_object(
        cls,
        model: str = None,
        name: str = None,
        description: str = None,
        instructions: str = None,
        tools: Optional[str] = [],
        file_ids: Optional[str] = [],
        metadata: Dict = {},
    ):
        obj = {}
        if model:
            obj['model'] = model
        if name:
            obj['name'] = name
        if description:
            obj['description'] = description
        if instructions:
            obj['instructions'] = instructions
        if tools:
            obj['tools'] = tools
        obj['file_ids'] = file_ids
        obj['metadata'] = metadata

        return obj

    @classmethod
    def call(cls,
             *,
             model: str,
             name: str = None,
             description: str = None,
             instructions: str = None,
             tools: Optional[List[Dict]] = [],
             file_ids: Optional[List[str]] = [],
             metadata: Dict = None,
             workspace: str = None,
             api_key: str = None,
             **kwargs) -> Assistant:
        """Create Assistant.

        Args:
            model (str): The model to use.
            name (str, optional): The assistant name. Defaults to None.
            description (str, optional): The assistant description. Defaults to None.
            instructions (str, optional): The system instructions this assistant uses. Defaults to None.
            tools (Optional[List[Dict]], optional): List of tools to use. Defaults to [].
            file_ids (Optional[List[str]], optional): : The files to use. Defaults to [].
            metadata (Dict, optional): Custom key-value pairs associate with assistant. Defaults to None.
            workspace (str, optional): The DashScope workspace id. Defaults to None.
            api_key (str, optional): The DashScope api key. Defaults to None.

        Raises:
            ModelRequired: The model is required.

        Returns:
            Assistant: The `Assistant` object.
        """
        return cls.create(model=model,
                          name=name,
                          description=description,
                          instructions=instructions,
                          tools=tools,
                          file_ids=file_ids,
                          metadata=metadata,
                          workspace=workspace,
                          api_key=api_key,
                          **kwargs)

    @classmethod
    def create(cls,
               *,
               model: str,
               name: str = None,
               description: str = None,
               instructions: str = None,
               tools: Optional[List[Dict]] = [],
               file_ids: Optional[List[str]] = [],
               metadata: Dict = None,
               workspace: str = None,
               api_key: str = None,
               **kwargs) -> Assistant:
        """Create Assistant.

        Args:
            model (str): The model to use.
            name (str, optional): The assistant name. Defaults to None.
            description (str, optional): The assistant description. Defaults to None.
            instructions (str, optional): The system instructions this assistant uses. Defaults to None.
            tools (Optional[List[Dict]], optional): List of tools to use. Defaults to [].
            file_ids (Optional[List[str]], optional): : The files to use. Defaults to [].
            metadata (Dict, optional): Custom key-value pairs associate with assistant. Defaults to None.
            workspace (str, optional): The DashScope workspace id. Defaults to None.
            api_key (str, optional): The DashScope api key. Defaults to None.

        Raises:
            ModelRequired: The model is required.

        Returns:
            Assistant: The `Assistant` object.
        """
        if not model:
            raise ModelRequired('Model is required!')
        data = cls._create_assistant_object(model, name, description,
                                            instructions, tools, file_ids,
                                            metadata)
        response = super().call(data=data,
                                api_key=api_key,
                                flattened_output=True,
                                workspace=workspace,
                                **kwargs)
        return Assistant(**response)

    @classmethod
    def retrieve(cls,
                 assistant_id: str,
                 *,
                 workspace: str = None,
                 api_key: str = None,
                 **kwargs) -> Assistant:
        """Get the `Assistant`.

        Args:
            assistant_id (str): The assistant id.
            workspace (str): The dashscope workspace id.
            api_key (str, optional): The api key. Defaults to None.

        Returns:
            Assistant: The `Assistant` object.
        """
        return cls.get(assistant_id,
                       workspace=workspace,
                       api_key=api_key,
                       **kwargs)

    @classmethod
    def get(cls,
            assistant_id: str,
            *,
            workspace: str = None,
            api_key: str = None,
            **kwargs) -> Assistant:
        """Get the `Assistant`.

        Args:
            assistant_id (str): The assistant id.
            workspace (str): The dashscope workspace id.
            api_key (str, optional): The api key. Defaults to None.

        Returns:
            Assistant: The `Assistant` object.
        """
        if not assistant_id:
            raise ModelRequired('assistant_id is required!')
        response = super().get(assistant_id,
                               workspace=workspace,
                               api_key=api_key,
                               flattened_output=True,
                               **kwargs)
        return Assistant(**response)

    @classmethod
    def list(cls,
             *,
             limit: int = None,
             order: str = None,
             after: str = None,
             before: str = None,
             workspace: str = None,
             api_key: str = None,
             **kwargs) -> AssistantList:
        """List assistants

        Args:
            limit (int, optional): How many assistant to retrieve. Defaults to None.
            order (str, optional): Sort order by created_at. Defaults to None.
            after (str, optional): Assistant id after. Defaults to None.
            before (str, optional): Assistant id before. Defaults to None.
            workspace (str, optional): The DashScope workspace id. Defaults to None.
            api_key (str, optional): Your DashScope api key. Defaults to None.

        Returns:
            AssistantList: The list of assistants.
        """
        response = super().list(limit=limit,
                                order=order,
                                after=after,
                                before=before,
                                workspace=workspace,
                                api_key=api_key,
                                flattened_output=True,
                                **kwargs)
        return AssistantList(**response)

    @classmethod
    def update(cls,
               assistant_id: str,
               *,
               model: str = None,
               name: str = None,
               description: str = None,
               instructions: str = None,
               tools: Optional[str] = [],
               file_ids: Optional[str] = [],
               metadata: Dict = None,
               workspace: str = None,
               api_key: str = None,
               **kwargs) -> Assistant:
        """Update an exist assistants

        Args:
            assistant_id (str): The target assistant id.
            model (str): The model to use.
            name (str, optional): The assistant name. Defaults to None.
            description (str, optional): The assistant description . Defaults to None.
            instructions (str, optional): The system instructions this assistant uses.. Defaults to None.
            tools (Optional[str], optional): List of tools to use.. Defaults to [].
            file_ids (Optional[str], optional): The files to use in assistants.. Defaults to [].
            metadata (Dict, optional): Custom key-value pairs associate with assistant. Defaults to None.
            workspace (str): The DashScope workspace id.
            api_key (str, optional): The DashScope workspace id. Defaults to None.

        Returns:
            Assistant: The updated assistant.
        """
        if not assistant_id:
            raise ModelRequired('assistant_id is required!')
        response = super().update(assistant_id,
                                  cls._create_assistant_object(
                                      model, name, description, instructions,
                                      tools, file_ids, metadata),
                                  api_key=api_key,
                                  workspace=workspace,
                                  flattened_output=True,
                                  method='post',
                                  **kwargs)
        return Assistant(**response)

    @classmethod
    def delete(cls,
               assistant_id: str,
               *,
               workspace: str = None,
               api_key: str = None,
               **kwargs) -> DeleteResponse:
        """Delete uploaded file.

        Args:
            assistant_id (str): The assistant id want to delete.
            workspace (str): The DashScope workspace id.
            api_key (str, optional): The api key. Defaults to None.

        Returns:
            AssistantsDeleteResponse: Delete result.
        """
        if not assistant_id:
            raise ModelRequired('assistant_id is required!')
        response = super().delete(assistant_id,
                                  api_key=api_key,
                                  workspace=workspace,
                                  flattened_output=True,
                                  **kwargs)
        return DeleteResponse(**response)
