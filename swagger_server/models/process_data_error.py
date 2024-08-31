# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ProcessDataError(Model):

    def __init__(self, code: str=None, message: str=None):  # noqa: E501
        """ProcessDataError - a model defined in Swagger

        :param code: The code of this ProcessDataError.  # noqa: E501
        :type code: str
        :param message: The message of this ProcessDataError.  # noqa: E501
        :type message: str
        """
        self.swagger_types = {
            'code': str,
            'message': str
        }

        self.attribute_map = {
            'code': 'code',
            'message': 'message'
        }
        self._code = code
        self._message = message

    @classmethod
    def from_dict(cls, dikt) -> 'ProcessDataError':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ProcessDataError of this ProcessDataError.  # noqa: E501
        :rtype: ProcessDataError
        """
        return util.deserialize_model(dikt, cls)

    @property
    def code(self) -> str:
        """Gets the code of this ProcessDataError.


        :return: The code of this ProcessDataError.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code: str):
        """Sets the code of this ProcessDataError.


        :param code: The code of this ProcessDataError.
        :type code: str
        """

        self._code = code

    @property
    def message(self) -> str:
        """Gets the message of this ProcessDataError.


        :return: The message of this ProcessDataError.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message: str):
        """Sets the message of this ProcessDataError.


        :param message: The message of this ProcessDataError.
        :type message: str
        """

        self._message = message
