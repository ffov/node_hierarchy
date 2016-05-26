#!/usr/bin/python
# -*- coding: utf-8 -
#Imports:
import urllib
import json
from pprint import pprint
from node import Node
from geocode import Geocode

class Graph:
	def __init__(self, nodesData, graphData):
		self.coder = Geocode(geocoderCache = True, printStatus = True)
		self.data = graphData
		self.nodes = nodesData
		self.nodes_list = {}
		self.nodes_no_autoupdater = {}
		self.nodes_no_geo = {}
		self.parseNodes()
		self.parseLinks()
		self.calculateStepsToVpn()
		self.findMissingGeo()

	def parseNodes(self):
		for k,v in self.nodes['nodes'].iteritems():
			lat, lon = self.getGeo(k)
			node = Node(k, ipv6 = self.getPublicAddress(k), hostname = self.getHostname(k), isOnline = self.getOnlineState(k), lat=lat, lon=lon, coder = self.coder, autoupdater = self.getAutoupdaterStatus(k), branch = self.getBranch(k), isGateway = self.getIsGateway(k), interfaces = self.getInterfaces(k))
			self.nodes_list[k] = node

	def parseLinks(self):
		link_nodes = self.data['batadv']['nodes']
		for link in self.data['batadv']['links']:
			if 'node_id' in link_nodes[link['source']] and 'node_id' in link_nodes[link['target']]:#else it is a vpn link
				if self.nodes_list[link_nodes[link['source']]['node_id']].isGateway == True or self.nodes_list[link_nodes[link['target']]['node_id']].isGateway:
					self.setVpnLink(link['source'], link['target'])
				else:
					self.setLinkBetween(link_nodes[link['source']], link_nodes[link['target']])
			else:
				self.setVpnLink(link['source'], link['target'])
	
	def getLinkType(self, interfaces, link_id):
		if not interfaces:
			return None
		for k, v in interfaces.iteritems():
			if link_id in v:
				return k

	def setLinkBetween(self, src, dst, stateOnline = True, lastSeen = None):
		src_id = src['node_id']
		dst_id = dst['node_id']
		src_type = self.getLinkType(self.nodes_list[src_id].interfaces, src['id'])
		dst_type = self.getLinkType(self.nodes_list[dst_id].interfaces, dst['id'])
		if dst_type == 'other' or src_type == 'other':
			print 'LAN Link: src:', self.nodes_list[src_id].hostname, 'dst:', self.nodes_list[dst_id].hostname

		if src_id and dst_id:
			self.nodes_list[src_id].links[dst_id] = {
				'node' : self.nodes_list[dst_id],
				'state_online' : stateOnline,
				'last_seen' : lastSeen,
				'type' : src_type
			}
			self.nodes_list[dst_id].links[src_id] = {
				'node' : self.nodes_list[src_id],
				'state_online' : stateOnline,
				'last_seen' : lastSeen,
				'type' : dst_type
			}

	def setVpnLink(self, src, dst):
		if 'node_id' not in self.data['batadv']['nodes'][src] or (self.data['batadv']['nodes'][src]['node_id'] and self.nodes_list[self.data['batadv']['nodes'][src]['node_id']].isGateway == True):
			if 'node_id' in self.data['batadv']['nodes'][dst] and self.data['batadv']['nodes'][dst]['node_id']:
				self.nodes_list[self.data['batadv']['nodes'][dst]['node_id']].stepsToVpn = 0
		elif 'node_id' not in self.data['batadv']['nodes'][dst] or (self.data['batadv']['nodes'][dst]['node_id'] and self.nodes_list[self.data['batadv']['nodes'][dst]['node_id']].isGateway == True):
			if 'node_id' in self.data['batadv']['nodes'][src] and self.data['batadv']['nodes'][src]['node_id']:
				self.nodes_list[self.data['batadv']['nodes'][src]['node_id']].stepsToVpn = 0

	def calculateStepsToVpn(self):
		for node in self.nodes_list.itervalues():
			node.calculateStepsToVpn()

	def findMissingGeo(self):
		for node in self.nodes_list.itervalues():
			node.findMissingGeo()

	def getAllLevelXNodes(self, level, online = True):
		zmap = {}
		for k,v in self.nodes_list.iteritems():
			if v.isOnline or online == False:
				if v.stepsToVpn == level:
					zmap[k] = v
		return zmap


	def getInterfaces(self, node_id):
		try:
			return self.nodes['nodes'][node_id]['nodeinfo']['network']['mesh']['bat0']['interfaces']
		except:
			return None #lecagy nodes or non well formed node

	def getHostname(self,node_id):
		return self.nodes['nodes'][node_id]['nodeinfo']['hostname']

	def getIsGateway(self,node_id):
		return self.nodes['nodes'][node_id]['flags']['gateway']

	def getAutoupdaterStatus(self, node_id):
		#return True
		if 'autoupdater' in self.nodes['nodes'][node_id]['nodeinfo']['software']:
			return self.nodes['nodes'][node_id]['nodeinfo']['software']['autoupdater']['enabled']
		else:
			#if node is offline for a long time sometimes no autoupdater status can be found
			return False

	def getBranch(self, node_id):
		#return True
		if 'autoupdater' in self.nodes['nodes'][node_id]['nodeinfo']['software']:
			return self.nodes['nodes'][node_id]['nodeinfo']['software']['autoupdater']['branch']
		else:
			#if node is offline for a long time sometimes no autoupdater status can be found
			return None

	def getGeo(self, node_id):
		if 'location' in self.nodes['nodes'][node_id]['nodeinfo'] and 'latitude' in self.nodes['nodes'][node_id]['nodeinfo']['location'] and 'longitude' in self.nodes['nodes'][node_id]['nodeinfo']['location']:
			return self.nodes['nodes'][node_id]['nodeinfo']['location']['latitude'], self.nodes['nodes'][node_id]['nodeinfo']['location']['longitude']
		return None, None

	def getPublicAddress(self,node_id):
		if node_id in self.nodes['nodes']:
			if 'addresses' in self.nodes['nodes'][node_id]['nodeinfo']['network']:
				for address in self.nodes['nodes'][node_id]['nodeinfo']['network']['addresses']:
					if address.startswith('2a03'):
						return address
		return None

	def getOnlineState(self,node_id):
		return self.nodes['nodes'][node_id]['flags']['online']

	def getProblemNodes(self, noAutoupdater = False, noGeodata = False, online = True):
		results = {}
		for k,v in self.nodes_list.iteritems():
			if v.isOnline or online == False:
				if noAutoupdater and noGeodata:
					if not v.autoupdater and not v.geodata:
						results[k] = v 
				elif noAutoupdater:
					if v.autoupdater and v.geodata:
						results[k] = v 
				elif noGeodata:
					if not v.geodata and v.autoupdater:
						results[k] = v
		return results


	def getNodeCloudsIn(self, region, branch = 'stable'):
		results = {}
#		noAuto = False
		for k,v in self.getAllLevelXNodes(0).iteritems():
			if v.isOnline == True:
				if v.geodata != None:
					if v.isInRegion(region):
						ncloud = v.getNodeCloud({})
						for ksub,vsub in ncloud.iteritems():
							if not vsub.autoupdater or (branch and vsub.branch != branch):
								break
						else:
							if self.isLANlinkInCloud(ncloud) == False:
								results.update(ncloud)
		print "Result:",len(results), region
		return results

	def isLANlinkInCloud(self, nodeCloud):
		for k,v in nodeCloud.iteritems():
			for ksub, vsub in v.links.iteritems():
				if k in self.nodes_list and ksub in self.nodes_list[k].links:
					if self.nodes_list[k].links[ksub]['type'] == 'other':
						return True
				if ksub in self.nodes_list and k in self.nodes_list[ksub].links:
					if self.nodes_list[ksub].links[k]['type'] == 'other':
						return True
		return False

	def maxDepth(self):
		maxDepth = 0
		for v in self.nodes_list.itervalues():
			if v.stepsToVpn > maxDepth:
				maxDepth = v.stepsToVpn
		return maxDepth+1