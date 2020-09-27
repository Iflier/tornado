# -*- coding:utf-8 -*-
"""
Dec: HTTPServer 类调用关系图
Created on: 2020.09.26
Author: Iflier
"""
import os
from graphviz import Digraph


graph = Digraph(comment="HTTPServer 类调用关系图", name="HTTPServer", engine='dot', format='png', directory=os.getcwd())
# graph2 = Digraph(comment="HTTPServerConnectionDelegate 类调用关系图", format='png', engine='dot')

graph.node("object", label="objct")
graph.node("Configurable", label="Configurable")
graph.node('TCPServer', label='TCPServer')
graph.node("http1connection.HTTP1ServerConnection", label="http1connection.HTTP1ServerConnection")
graph.node("httputil.HTTPServerConnectionDelegate", label="httputil.HTTPServerConnectionDelegate")
graph.node("HTTPServer", label="HTTPServer")

graph.edges([
    ("object", "TCPServer"),
    ("object", "Configurable"),
    ("object", "http1connection.HTTP1ServerConnection"),
    ("object", "httputil.HTTPServerConnectionDelegate")
    ])

graph.edges([
    ("TCPServer", "HTTPServer"),
    ("Configurable", "HTTPServer"),
    ("httputil.HTTPServerConnectionDelegate", "HTTPServer")
    ])

graph.node("start_serving", label="start_serving")
graph.node("_server_request_loop", label="concurrent _server_request_loop")
graph.edges([
    ("http1connection.HTTP1ServerConnection", "start_serving"),
    ("start_serving", "_server_request_loop")
    ])

graph.node("start_request", label="start_request\nImplement by subclass")
graph.edge("httputil.HTTPServerConnectionDelegate", "start_request", label="Implement by subclass")

graph.node("handle_stream", label="handle_stream\nInstantiation HTTP1ServerConnection class,\ncall it's start_serving method")
graph.node("close_all_connections", label="concurrent close_all_connections\nClose each connections from self.__connections")
graph.edge("TCPServer", "handle_stream", label="Implement by subclass")
graph.edges([
    ("HTTPServer", "handle_stream"),
    ("HTTPServer", "start_request"),
    ("HTTPServer", "close_all_connections"),
    ("handle_stream", "start_serving")
    ])

graph.render(filename="HTTPServerCallView.vg", view=True)
