# -*- coding:utf-8 -*-
"""
Dec: TCPServer 类调用关系图
Created on: 2020.09.24
Author: Iflier
"""
import os

from graphviz import Digraph


graph = Digraph(name="TCPServer", format='png', comment="TCPServer 调用关系图", directory=os.getcwd(), engine='dot', filename="TCPServerCallView")

graph.node("object", label='object')
graph.node("bind_sockets", label="netutil::bind_sockets\nreturn a list of socket.socket objects bind to given a address")
graph.node("TCPServer", label='TCPServer')
graph.edge("object", "TCPServer")

graph.node('start', label="start\nCall add_sockets\nself._started=True")
graph.node("stop", label="stop\nClose each socket.socket and unregister handlers associated\nwith each socket.socket's fd in self._sockets and IOLoop respectively")
graph.node("bind", label="bind\nCall bind_sockets creat a list of socket.socket objects for passed address and port args,\nthen call add_sockets if self._started")

graph.node("listen", label="listen\nUse given address and port args to create a list of socket.socket objects,\nthen call add_sockets")
graph.node("add_sockets", label="add_sockets\nCall self._handle_connection to handle each connection from\nthe other end for each socket.socket object in passed socket.socket list")
graph.node("add_accept_handler", label="netutil::add_accept_handler")
graph.node("_handle_connection", label="_handle_connection\nCreate an IOStream instance for passed socket.socket object,\ncall self.handle_stream to create a Future object and then add to EventLoop")
graph.node("handle_stream", label="handle_stream\nImplement by subclass")

graph.edges([('TCPServer', 'listen'), ("TCPServer", "start"), ("TCPServer", "stop"), ('TCPServer', 'bind')])
# graph.edges([('TCPServer', 'listen'), ("TCPServer", "start"), ("TCPServer", "stop"), ('TCPServer', 'bind'), ('TCPServer', 'add_sockets')])
graph.edge("listen", "bind_sockets", label="step 1")
graph.edge("listen", "add_sockets", label="step 2")

graph.edge("bind", "bind_sockets", label="step 1")
graph.edge("bind", "add_sockets", label="step 2: if self._started")

graph.edges([('start', 'add_sockets')])
graph.edge("add_sockets", "add_accept_handler", label="Call for each socket.socket")
graph.edge("add_accept_handler", "_handle_connection")
graph.edge("_handle_connection", "handle_stream")

graph.render(filename="tcpserver.vg", view=True)
