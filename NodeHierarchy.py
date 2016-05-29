#!/usr/bin/python3
import argparse
from parser.NodesParser import NodesParser
from parser.GraphParser import GraphParser
from cloud.Node import Node
from cloud.Link import Link
from cloud.GlobalGraph import GlobalGraph
from parser.ShapesParser import ShapesParser
from cloud.Domaene import Domaene
from generator.NginxConfGen import NginxConfGen

class NodeHierarchy(object):
    def __init__(self):
        self.__args__ = self.__parseArguments__()
        self.__nodesJson__ = NodesParser(self.__args__.json_path)
        self.__graphJson__ = GraphParser(self.__args__.json_path)
        self.__shapesJson__ = self.__parseShapes__()
        self.nodes = self.__createNodeObjects__()
        self.links = self.__createLinkObjects__()
        self.globalGraph = self.__createGlobalGraph__()
        self.domains = self.__createDomains__()
        self.nginxConf = NginxConfGen(self.domains, self.__args__)
        self.nginxConf.writeNginxConfigFile()

    def __parseShapes__(self):
        shapesJson = {}
        for targetName in self.__args__.targets:
            shapesJson[targetName] = ShapesParser(self.__args__.shapes_path, targetName)
        return shapesJson

    def __createDomains__(self):
        domains = {}
        for k, v in self.__shapesJson__.items():
            print('Create Domain object #',len(domains), '\r',end = '')
            domains[k] = Domaene(k,v, self.globalGraph)
        print('')
        return domains

    def __createNodeObjects__(self):
        nodes = {}
        for nodeID, nodeValue in self.__nodesJson__.nodes.items():
            print('Create Node object #',len(nodes), '\r',end = '')
            nodes[nodeID] = Node(nodeValue)
        print('')
        return nodes
    
    def __createLinkObjects__(self):
        links = []
        for link in self.__graphJson__.links:
            try:
                srcNode = self.nodes[link['source']['node_id']]
            except:
                srcNode = None
            try:
                dstNode = self.nodes[link['target']['node_id']]
            except:
                dstNode = None
            
            print('Create Link object #',len(links), '\r',end = '')
            links.append(Link(link, srcNode, dstNode))
        print('')
        return links
            
    def __createGlobalGraph__(self):
        return GlobalGraph(self.nodes, self.links, self.__args__.debug)

    def __parseArguments__(self):
        parser = argparse.ArgumentParser(description='This Script generates a hierarchical nodes list for node migration using nginx geo feature.')
        parser.add_argument('-j', '--json-path', required=False, default='https://service.freifunk-muensterland.de/maps/data/', help='Path of nodes.json and graph.json (can be local folder or remote URL).')
        parser.add_argument('-s', '--shapes-path', required=False, default='https://freifunk-muensterland.de/md-fw-dl/shapes/', help='Path of shapefiles (can be local folder or remote URL).')
        parser.add_argument('-t', '--targets', nargs='+', required=True, help='List of targets which should be proceeded. Example: -t citya cityb ...')
        parser.add_argument('-o', '--out-file', required=False, help='Filename where the generated Output should stored.', default='./webserver-configuration')
        parser.add_argument('-v', '--debug', required=False, action='store_true', help='Enable debugging output.')
        parser.add_argument('-f', '--filters', nargs='*', required=False, help='Filter out nodes and local clouds based on filter rules')
        
        return parser.parse_args()

NodeHierarchy()
