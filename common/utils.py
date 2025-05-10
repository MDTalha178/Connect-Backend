import random

from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet


class CustomResponse(Response):
    """
    Custom Response class to standardize the format of responses.

    This subclass of the `Response` class modifies the default response format to include:
    - `status_code`: The HTTP status code.
    - `data`: The actual data returned in the response.

    It ensures that every response from the API follows a consistent format, regardless of success or failure.
    """

    def __init__(self, data=None, status_code=None, **kwargs):
        """
        Initializes the custom response with a standardized structure.

        :param data: The main data to return in the response.
        :param status_code: The HTTP status code for the response (e.g., 200 for success).
        :param kwargs: Additional keyword arguments passed to the base `Response` class.
        """
        # Modify the data structure to include status_code and data
        data = {'status_code': status_code, 'data': data}
        # Call the parent constructor with the formatted data
        super().__init__(data, **kwargs)


class CustomAPIResponseMixin:
    """
    Mixin that provides standard methods to return success and failure responses.

    This mixin can be added to view classes to standardize the format of responses sent from the API.
    It provides two methods:
    - `success_response`: Returns a success response with the given data and status.
    - `failure_response`: Returns a failure response with the given data and status.

    The response format ensures consistency in the way responses are structured across the application.
    """

    # Class-level constants to indicate success or failure status
    __SUCCESS = "success"
    __FAILURE = "failure"

    @classmethod
    def success_response(cls, data=None, message=None, status_code=status.HTTP_200_OK, **kwargs):
        """
        Returns a standardized success response.

        The response includes the following structure:
        {
            "status": "success",
            "status_code": <HTTP status code>,
            "message": <Optional message>,
            "data": <Optional data>
        }

        :param data: The data to include in the response (optional).
        :param message: A message to include in the response (optional).
        :param status_code: The HTTP status code (default is 200 OK).
        :return: A custom response object with success status.
        """
        # Construct the response data structure
        response_data = {
            'status': cls.__SUCCESS,
            'status_code': status_code
        }
        # Add optional message and data to the response
        if message is not None:
            response_data['message'] = message

        for key, val in kwargs.items():
            response_data[key] = val

        if data is not None:
            response_data['data'] = data

        # Return a CustomResponse object with the formatted data
        return CustomResponse(data=response_data, status_code=status_code)

    @classmethod
    def failure_response(cls, data=None, message=None, status_code=status.HTTP_400_BAD_REQUEST):
        """
        Returns a standardized failure response.

        The response includes the following structure:
        {
            "status": "failure",
            "status_code": <HTTP status code>,
            "message": <Optional message>,
            "data": <Optional data>
        }

        :param data: The data to include in the response (optional).
        :param message: A message to include in the response (optional).
        :param status_code: The HTTP status code (default is 400 Bad Request).
        :return: A Response object with failure status.
        """
        # Construct the response data structure for failure
        response_data = {
            "status_code": status_code,
            "status": cls.__FAILURE
        }

        # Add optional message and data to the response
        if message is not None:
            response_data["message"] = message

        if data is not None:
            response_data["data"] = data

        # Return a standard Response object with failure data
        return Response(response_data, status=status_code)


class CustomModelView(ModelViewSet, CustomAPIResponseMixin):
    """
    Custom ViewSet that integrates the `CustomAPIResponseMixin`.

    This class extends `ModelViewSet` to provide default CRUD operations for a model,
    and includes the response formatting provided by the `CustomAPIResponseMixin`.

    It allows you to return standardized success or failure responses from your API
    without needing to define response structure for each individual view.

    Example usage:
    - Inherit this class and call `success_response` or `failure_response` from your actions.
    """
    pass