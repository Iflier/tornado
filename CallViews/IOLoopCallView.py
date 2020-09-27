# -*- coding:utf-8 -*-
"""
Dec: 绘制 IOLoop 类调用关系图
Created on: 2020.09.23
Author: Iflier
"""
import os

from graphviz import Digraph

graph = Digraph(comment="IOLoop 类调用关系图", format='png', filename="IOLoopCallView", directory=os.getcwd(), engine='dot')

graph.node("object", "object")
graph.node("Configurable", "util::Configurable")
graph.node("BaseAsyncIOLoop", label="platform::asyncio::BaseAsyncIOLoop")
graph.node("AsyncIOLoop", label="platform::asyncio::AsyncIOLoop")

graph.edges([
    ("object", 'Configurable'),
    ("Configurable", 'IOLoop'),  # class IOLoop inherited from Configurable
    ("IOLoop", "BaseAsyncIOLoop"),  # class BaseAsyncIOLoop inherited from IOLoop
    ("BaseAsyncIOLoop", "AsyncIOLoop")
    ])

graph.node("IOLoop", label="ioloop::IOLoop")
# an instance attribute
graph.node("_ioloop_for_asyncio", label="instance attribute\n_ioloop_for_asyncio\ntype=dict")
graph.node("instance", label="instance\nreturn IOLoop.current()")
graph.node("current", label='staticmethod:current\nreturn: An asyncio.get_event_loop object')
graph.node("add_future", label="add_future")
graph.node("add_done_callback", label="Call Future's add_done_callback")
graph.node("future_add_done_callback", label="concurrent::future_add_done_callback")

graph.edges([
    ("IOLoop", '_ioloop_for_asyncio'),
    ("IOLoop", 'current'),
    ("IOLoop", "instance"),
    ("IOLoop", "add_future")
    ])

graph.edge("add_future", "add_done_callback", label="if is a Future instance")
graph.edge("add_future", "future_add_done_callback", label="if is not a Future instance")

graph.node("start", label="start\ncall self.asyncio_loop.run_forever()")
graph.node("stop", label="stop\ncall self.asyncio_loop.stop()")
graph.node("close", label="close\nremove self.asyncio_loop from _ioloop_for_asyncio\nself.asyncio_loop.close()")
graph.node("add_handler", label="add_handler\nCall self.asyncio_loop.add_reader / add_writer")
graph.node("make_current", label="make_current\ncall asyncio.set_event_loop(self.asyncio_loop)\nself.is_current = True")

graph.edges([("BaseAsyncIOLoop", "start"),
             ("BaseAsyncIOLoop", "stop"),
             ("BaseAsyncIOLoop", "close"),
             ("BaseAsyncIOLoop", "add_handler"),
             ("AsyncIOLoop", 'make_current')
             ])

graph.render(filename='IOLoop.vg', view=True)
