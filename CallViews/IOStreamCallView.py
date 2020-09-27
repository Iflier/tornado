# -*- coding:utf-8 -*-
"""
Dec: IOStream 类调用关系图
Created on: 2020.09.26
Author: Iflier
"""
import os

from graphviz import Digraph
from graphviz.backend import view


graph = Digraph(comment="IOStream 类调用关系图", format='png', engine='dot', directory=os.getcwd(), filename="IOStreamCallView")

graph.node("object", label="object")
graph.node("BaseIOStream", label="BaseIOStream")
graph.node("IOStream", label="IOStream")
graph.node("BaseAsyncIOLoop", label="BaseAsyncIOLoop")
graph.edges([('object', "BaseIOStream"), ("BaseIOStream", "IOStream")])

graph.node("add_handler", label="add_handler\nMonitor fd, call add_reader or add_writer")
graph.node("update_handler", label="update_handler")

graph.node("closed_fd", label="close_fd\nCall socket.socket object's close() method")
graph.node("read_from_fd", label="read_from_fd\nReceive content from self.sock,\nreturn received bytes number")
graph.node("write_to_fd", label="write_to_fd\nCall self.socket.send() medthod")
graph.node("connect", label="connect\nConnect to passed address,\nthen call super()._add_io_state\nreturn a Future object")
graph.node("_add_io_state", label="_add_io_state\nCall add_handler or update_handler")

# BaseAsyncIOLoop 类的方法
graph.edges([("BaseAsyncIOLoop", 'add_handler'), ("BaseAsyncIOLoop", "update_handler")])

graph.edge("BaseIOStream", "_add_io_state")
graph.edges([("IOStream", "closed_fd"),
             ("IOStream", "read_from_fd"),
             ("IOStream", "write_to_fd"),
             ("IOStream", "connect")])
graph.edge("connect", "_add_io_state")
graph.edge("_add_io_state", "add_handler", label="if self._state is None")
graph.edge("_add_io_state", "update_handler", label="if not self._state & state")
graph.render(filename="IOStreamCallView.vg", view=True)
