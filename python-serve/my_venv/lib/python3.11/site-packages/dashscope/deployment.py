from dashscope.api_entities.dashscope_response import DashScopeAPIResponse
from dashscope.client.base_api import (CreateMixin, DeleteMixin, GetMixin,
                                       ListMixin, PutMixin, StreamEventMixin)


class Deployment(CreateMixin, DeleteMixin, ListMixin, GetMixin,
                 StreamEventMixin, PutMixin):
    SUB_PATH = 'deployments'
    """Deploy a model.
    """
    @classmethod
    def call(cls,
             model: str,
             capacity: int,
             version: str = None,
             suffix: str = None,
             api_key: str = None,
             workspace: str = None,
             **kwargs) -> DashScopeAPIResponse:
        """Call to deployment a model service.

        Args:
            model (str): The model name.
            version (str, optional): The model version, unnecessary
                for fine-tuned model. Defaults to None.
            suffix (str, optional): The name suffix of the model deployment,
                If specified, the final model name will be model_suffix.
                Defaults to None.
            capacity (int, optional): The model service capacity.
            api_key (str, optional): The api-key. Defaults to None.
            workspace (str): The dashscope workspace id.

        Returns:
            DashScopeAPIResponse: _description_
        """
        req = {'model_name': model, 'capacity': capacity}

        if version is not None:
            req['model_version'] = version
        if suffix is not None:
            req['suffix'] = suffix
        return super().call(req,
                            api_key=api_key,
                            workspace=workspace,
                            **kwargs)

    @classmethod
    def list(cls,
             page_no=1,
             page_size=10,
             api_key: str = None,
             workspace: str = None,
             **kwargs) -> DashScopeAPIResponse:
        """List deployments.

        Args:
            api_key (str, optional): The api api_key, if not present,
                will get by default rule(TODO: api key doc). Defaults to None.
            page_no (int, optional): Page number. Defaults to 1.
            page_size (int, optional): Items per page. Defaults to 10.
            workspace (str): The dashscope workspace id.

        Returns:
            DashScopeAPIResponse: The deployment list.
        """
        return super().list(page_no,
                            page_size,
                            api_key,
                            workspace=workspace,
                            **kwargs)

    @classmethod
    def get(cls,
            deployed_model: str,
            api_key: str = None,
            workspace: str = None,
            **kwargs) -> DashScopeAPIResponse:
        """Get model deployment information.

        Args:
            deployed_model (str): The deployment_id.
            api_key (str, optional): The api key. Defaults to None.
            workspace (str): The dashscope workspace id.

        Returns:
            DashScopeAPIResponse: The deployment information.
        """
        return super().get(deployed_model,
                           api_key,
                           workspace=workspace,
                           **kwargs)

    @classmethod
    def delete(cls,
               deployment_id: str,
               api_key: str = None,
               workspace: str = None,
               **kwargs) -> DashScopeAPIResponse:
        """Delete model deployment.

        Args:
            deployment_id (str): The deployment id.
            api_key (str, optional): The api key. Defaults to None.
            workspace (str): The dashscope workspace id.

        Returns:
            DashScopeAPIResponse: The delete result.
        """
        return super().delete(deployment_id,
                              api_key,
                              workspace=workspace,
                              **kwargs)

    @classmethod
    def update(cls,
               deployment_id: str,
               version: str,
               api_key: str = None,
               workspace: str = None,
               **kwargs) -> DashScopeAPIResponse:
        """Update model deployment.

        Args:
            deployment_id (str): The deployment id.
            version (str): The target model version.
            api_key (str, optional): The api key. Defaults to None.
            workspace (str): The dashscope workspace id.

        Returns:
            DashScopeAPIResponse: The delete result.
        """
        req = {'deployment_model': deployment_id, 'model_version': version}
        return super().put(deployment_id,
                           req,
                           api_key,
                           workspace=workspace,
                           **kwargs)

    @classmethod
    def scale(cls,
              deployment_id: str,
              capacity: int,
              api_key: str = None,
              workspace: str = None,
              **kwargs) -> DashScopeAPIResponse:
        """Scaling model deployment.

        Args:
            deployment_id (str): The deployment id.
            capacity (int): The target service capacity.
            api_key (str, optional): The api key. Defaults to None.

        Returns:
            DashScopeAPIResponse: The delete result.
        """
        req = {'deployed_model': deployment_id, 'capacity': capacity}
        path = '%s/%s/scale' % (cls.SUB_PATH.lower(), deployment_id)
        return super().put(deployment_id,
                           req,
                           path=path,
                           api_key=api_key,
                           workspace=workspace,
                           **kwargs)
