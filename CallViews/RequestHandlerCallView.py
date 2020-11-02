# -*- coding:utf-8 -*-
"""
Dec: RequestHandler 类调用关系图
Created on: 2020.09.27
Author: Iflier
"""
import os

from graphviz import Digraph


graph = Digraph(comment="RequestHandler 类调用关系图", format='png', engine='dot', directory=os.getcwd())

# class RequestHandler inherited from object 
graph.node("object", label="object")
graph.node("RequestHandler", label="RequestHandler")
graph.edge("object", "RequestHandler")

# RequestHandler class methods
graph.node("_header", label="self._header\nInitialized by self.clear(),an\nhttputil.HTTPHeaders instance")
graph.node("prepare", label="prepare\nCalled at the begining of any request type")
graph.node("on_finish", label="on_finish\nImplement by subclass,\ncalled after the end of a request")
graph.node("on_connection_close", label="on_connection_close\nClean up resources, called in async handlers\nif the client closed the connection")
graph.node("clear", label="clear\nReset all headers and content for this response")
graph.node("set_default_headers", label="set_default_headers\nImplement by subclass")
graph.node("set_status", label="set_status\nSets the status code for response\nSets self._status_code and self._reason")
graph.node("get_status", label="get_status\nreturn self._status_code")
graph.node("set_header", label="set_header\nCall self._convert_header_value,\nadd a new key-value pair to self._headers")
graph.node("add_header", label="add_header\nAdds the given response header and value to self._headers")
graph.node("clear_header", label="clear_header\nCleans an outgoing header")
graph.node("_convert_header_value", label="_convert_header_value\nConvert passed value to a string")
graph.node("get_argument", label="get_argument\nCall self._get_argument")
graph.node("get_arguments", label="get_arguments\nCall self._get_arguments, return a list")
graph.node("get_body_argument", label="get_body_argument\nCall self._get_argument")
graph.node("get_body_arguments", label="get_body_arguments\nCall self._get_arguments, return a list")
graph.node("get_query_argument", label="get_query_argument\nCall self._get_argument")
graph.node("get_query_arguments", label="get_query_arguments\nCall self._get_arguments, return a list")
graph.node("_get_argument", label="_get_argument\nCall self._get_arguments, return the last element in list")
graph.node("_get_arguments", label="_get_arguments\nReturn a list")
graph.node("set_cookie", label="set_cookie\nSets an outgoing cookie name/value with the given options")
graph.node("clear_cookie", label="clear_cookie\nDeletes the cookie with the given name")
graph.node("clear_all_cookies", label="clear_all_cookies\nDeletes all the cookies the user sent with this request")
graph.node("create_signed_value", label="create_signed_value")
graph.node("set_secure_cookie", label="set_secure_cookie\nCall set_cookie, create_signed_value")
graph.node("web.create_signed_value", label="web.create_signed_value")
graph.node("get_secure_cookie", label="get_secure_cookie\nCall web.decode_signed_value")
graph.node("redirect", label="redirect\nCall set_status, set_header and finish funcs")
graph.node("write", label="write\nWrites the given chunk to the output buffer")
graph.node("finish", label="finish\nFinishes this response, ending the HTTP request")
graph.node("current_user", label="current_user\nCall self.get_current_user")
graph.node("get_current_user", label="get_current_user\nOverride by subclass")
graph.node("get_login_url", label="get_login_url\nCan be overrided by subclass, default\nreturn value of \"login_url\" from self.application.settings")
graph.node("require_setting", label="require_setting\nRaises an exception if the given app setting is not defined")
graph.node("compute_etag", label="compute_etag\nUse hashlib compute SHA128 value of data in self._write_bufer")
graph.node("web._create_signature_v1", label="web._create_signature_v1\nUse hmac compute SHA128 value of all the passed args")


graph.edges([
    ("RequestHandler", "_header"),
    ("RequestHandler", "prepare"),
    ("RequestHandler", "on_finish"),
    ("RequestHandler", "on_connection_close"),
    ("RequestHandler", "clear"),
    ("clear", "set_default_headers"),
    ("RequestHandler", "set_default_headers"),
    ("RequestHandler", "set_status"),
    ("RequestHandler", "get_status"),
    ("RequestHandler", "_convert_header_value"),
    ("RequestHandler", "set_header"),
    ("set_header", "_convert_header_value"),
    ("RequestHandler", "add_header"),
    ("RequestHandler", "clear_header"),
    ("RequestHandler", "get_argument"),
    ("get_argument", "_get_argument"),
    ("RequestHandler", "get_arguments"),
    ("get_arguments", "_get_arguments"),
    ("RequestHandler", "get_body_argument"),
    ("get_body_argument", "_get_argument"),
    ("RequestHandler", "get_body_arguments"),
    ("get_body_arguments", "_get_arguments"),
    ("RequestHandler", "get_query_argument"),
    ("get_query_argument", "_get_argument"),
    ("RequestHandler", "get_query_arguments"),
    ("get_query_arguments", "_get_arguments"),
    ("RequestHandler", "_get_argument"),
    ("RequestHandler", "_get_arguments"),
    ("_get_argument", "_get_arguments"),
    ("RequestHandler", "set_cookie"),
    ("RequestHandler", "clear_cookie"),
    ("RequestHandler", "clear_all_cookies"),
    ("RequestHandler", "set_secure_cookie"),
    ("RequestHandler", "create_signed_value"),
    ("create_signed_value", "web.create_signed_value"),
    ("RequestHandler", "get_secure_cookie"),
    ("RequestHandler", "redirect"),
    ("RequestHandler", "write"),
    ("RequestHandler", "finish"),
    ("RequestHandler", "current_user"),
    ("RequestHandler", "get_current_user"),
    ("current_user", "get_current_user"),
    ("RequestHandler", "get_login_url"),
    ("RequestHandler", "require_setting"),
    ("RequestHandler", "compute_etag"),
])

# func create_signed_value will call set_cookie and create_signed_value funcs
graph.edges([
    ("set_secure_cookie", "set_cookie"),
    ("set_secure_cookie", "create_signed_value")
])

graph.edge("web.create_signed_value", "web._create_signature_v1", label="If version == 1\nCall web._create_signature_v1, connect value, timestamp and signature with b\"|\"")
graph.edge("web.create_signed_value", "web._create_signature_v2", label="If version == 2\nCall web._create_signature_v2")

# func redirect call set_status, set_header and finish funcs
graph.edges([
    ("redirect", "set_status"),
    ("redirect", "set_header"),
    ("redirect", "finish")
])

graph.edge("finish", "write", label="if `chunk` is not None")

graph.render(filename="RequestHandlerCallView.vg", view=True)
