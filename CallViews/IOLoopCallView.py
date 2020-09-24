# -*- coding:utf-8 -*-
"""
Dec: 绘制 IOLoop 类调用关系图
Created on: 2020.09.23
Author: Iflier
"""
import os

from graphviz import Digraph

graph = Digraph(comment="IOLoop 类调用关系图", format='png', filename="IOLoopCallView.png", directory=os.getcwd(), engine='dot')

graph.node("object", "object")
graph.node("Configurable", "util::Configurable")
graph.edge("object", 'Configurable')

# class IOLoop inherited from Configurable
graph.edge("Configurable", 'IOLoop')
graph.node("IOLoop", label="ioloop::IOLoop")
# an instance attribute
graph.node("_ioloop_for_asyncio", label="instance attribute\n_ioloop_for_asyncio\ntype=dict")
graph.node("instance", label="instance\nreturn IOLoop.current()")
graph.node("current", label='staticmethod:current\nreturn: An asyncio.get_event_loop object')
graph.edge("IOLoop", '_ioloop_for_asyncio')
graph.edge("IOLoop", 'current')
graph.edge("IOLoop", "instance")

# class BaseAsyncIOLoop inherited from IOLoop
graph.edge("IOLoop", "BaseAsyncIOLoop")
graph.node("BaseAsyncIOLoop", label="platform::asyncio::BaseAsyncIOLoop")
graph.node("start", label="start\ncall self.asyncio_loop.run_forever()")
graph.node("stop", label="stop\ncall self.asyncio_loop.stop()")
graph.node("close", label="close\nremove self.asyncio_loop from _ioloop_for_asyncio\nself.asyncio_loop.close()")

graph.node("AsyncIOLoop", label="platform::asyncio::AsyncIOLoop")
graph.node("make_current", label="make_current\ncall asyncio.set_event_loop(self.asyncio_loop)\nself.is_current = True")
graph.edge("AsyncIOLoop", 'make_current')
graph.edge("BaseAsyncIOLoop", "AsyncIOLoop")
graph.edge("BaseAsyncIOLoop", "start")
graph.edge("BaseAsyncIOLoop", "stop")
graph.edge("BaseAsyncIOLoop", "close")

graph.render(filename='IOLoop.vg', view=True)
