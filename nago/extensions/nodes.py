# -*- coding: utf-8 -*-

""" Management around connected nodes """

import nago.core
from nago.core import nago_access
import nago.extensions.settings

@nago_access
def list(search="unsigned"):
    """ List all connected nodes
    """
    nodes = nago.core.get_nodes()
    if search == "all":
        return nodes
    elif search == 'unsigned':
        result = {}
        for token, node in nodes.items():
            if node.get('access') is None:
                result[token] = node
        return result
    else:
        result = {}
        for token, node in nodes.items():
            host_name = node.get('host_name')
            if search in (token, host_name):
                result[token] = node
        return result

@nago_access
def sign(node=None):
    """ Sign a specific node to grant it access

     you can specify "all" to sign all nodes

     returns the nodes that were signed
    """
    if not node:
        raise Exception("Specify either 'all' your specify token/host_name of node to sign. ")
    if node == 'all':
        node = 'unsigned'
    nodes = list(search=node)
    result = {}
    for token, i in nodes:
        i['access'] = 'node'
        i.save()
        result[token] = i
    return result

@nago_access
def set(token_or_hostname, **kwargs):
    """ Change the attributes of a connected node """
    node = nago.core.get_node(security_token) or {}
    if not kwargs:
        return "No changes made"
    for k, v in kwargs.items():
        node[k] = v
    node.save()
    return "Saved %s changes" % len(kwargs)

@nago_access
def connect(token_or_hostname=None):
    """ Connect to another node. By default connect to the masternode """
    if token_or_hostname is None:
        token_or_hostname = nago.extensions.settings.get('server')
    node = nago.core.get_node(token_or_hostname)
    if not node:
        try:
            address = socket.gethostbyname(token_or_hostname)
            node = nago.core.Node()
            node['host_name'] = token_or_hostname
            node['address'] = address
        except Exception:
            raise Exception("'%s' was not found in list of known hosts, and does not resolve to a valid address" % token_or_hostname)
    node.send_command('test', 'connectivity')