#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for SEQing"""
import unittest
import dashboard_binding_sites as db
import json
import dash_html_components as html

class TestDashboard(unittest.TestCase):
    def testFormatChangeiCLIP(self):
        self.maxDiff = None
        null = None
        for test in ['svg', 'png']:
            self.assertEqual(eval(db.changeFormatiCLIP(test)), 
                {'response': {'props': {'config':{'toImageButtonOptions' : {'filename' : 'iCLIP', 'width' : None,
                'scale' : 1.0, 'height' : None, 'format' : test} }}}})
  
    def testFormatChangeRNA(self):
        self.maxDiff = None
        null = None
        for test in ['svg', 'png']:
            self.assertEqual(eval(db.changeFormatRNA(test)), 
                {'response': {'props': {'config':{'toImageButtonOptions' : {'filename' : 'RNA', 'width' : None,
                'scale' : 1.0, 'height' : None, 'format' : test} }}}})
    
    def testChangeLegendSpacing(self):
        self.maxDiff = None
        for test in [0, 0.1, 0.2, 0.3]:
            self. assertEqual(eval(db.changeLegendSpacing(test)),  {'response': {'props': {'children':str(test)}}} )
    
    def testShowHelpPopup(self):
        self.maxDiff = None
        null = None
        testVals = [((0,1),{'response': {'props': {'style': {"display": "none"}}}}),
                    ((1,0),{'response': {'props': {'style': {"display": "block"}}}}),
                    ((1,1),{'response': {'props': {'style': {"display": "none"}}}})]
        for test in testVals:
            self.assertEqual(eval(db.showHelpPopup(test[0][0],test[0][1])),test[1])
            
    def testConirmColor(self):
        testCases = []
        testCases.append(('test', json.dumps({'test' :'rgb(0,0,0)'}), {'test' : 'rgb(23, 23, 23)'}, (23,23,23)))
        testCases.append(('test', json.dumps({'test' :'rgb(0,0,0)'}), {'test' :'rgb(0,0,0)'} , (None,23,23)))
        testCases.append(('test', json.dumps({'test' :'rgb(0,0,0)'}), {'test' :'rgb(0,0,0)'}, (23,None,23)))
        testCases.append(('test', json.dumps({'test' :'rgb(0,0,0)'}), {'test' :'rgb(0,0,0)'}, (23,23,None)))
        testCases.append(('set2', json.dumps({'set2' :'rgb(0,0,0)'}), {'set2' : 'rgb(244, 23, 23)'}, (244,23,23)))
        for i in testCases:
            self.assertEqual(eval(db.confirmColor(0, i[3][0], i[3][1], i[3][2], i[0], i[1])),{'response': {'props': {'children' : json.dumps(i[2])}}} ) 
    
    def testChangeColor(self):
        testCases = []
        testCases.append(('test',(22,34,134), json.dumps({'test' :'rgb(0,0,0)'}), {'test' :'rgb(22, 34, 134)'}))
        testCases.append(('test',(22,None,134), json.dumps({'test' :'rgb(0,0,0)'}), {'test' :'rgb(0,0,0)'}))
        testCases.append(('test',(None,34,134), json.dumps({'test' :'rgb(0,0,0)'}), {'test' :'rgb(0,0,0)'}))
        testCases.append(('test',(22,34,None), json.dumps({'test' :'rgb(0,0,0)'}), {'test' :'rgb(0,0,0)'}))
        for i in testCases:
            self.assertEqual(eval(db.changeColor(i[1][0], i[1][1], i[1][2], i[0], i[2])),{'response': {'props': {'children' : json.dumps(i[3])}}})
    
    def testPreviewColorEvent(self):
        self.maxDiff = None
        self.assertEqual(eval(db.previewColorEvent(23, None, 66)),
            {'response': {'props': {'style': {'backgroundColor': 'rgb(255, 255, 255)', 'color': 'rgb(255, 255, 255)'}}}})
        self.assertEqual(eval(db.previewColorEvent(23, 48, 66)), 
            {'response': {'props': {'style': {'backgroundColor': 'rgb(23,48,66)', 'color': 'rgb(23,48,66)'}}}})
        
    def testOverlap(self):
        self.assertTrue(db.overlap((1,4),(2,7)))
        self.assertTrue(db.overlap((1,4),(1,4)))
        self.assertFalse(db.overlap((1,4),(1,1)))
        self.assertFalse(db.overlap((1,4),(5,7)))
        self.assertFalse(db.overlap((1,4),(4,7)))
    
    def testCreateDetailRow(self):
        testCases = []
        tableColors = ['rgb(0,0,0)', 'rgb(1,1,1)']
        testCases.append(('attribute', 'data', 1,  html.Tr(children=[html.Td(html.B('data'.replace('_', ' ').title())),
                                     html.Td(html.Table(children=
                                                        html.Tr(html.Td('attribute'.strip()))))],
                           style={'background-color': 'rgb(1,1,1)'}), None))
        testCases.append(('1;2;3;4;5;6', 'data', 2,  
                          html.Tr(children=[html.Td(html.B('data'.replace('_', ' ').title())),
                                    html.Td(html.Details(title = str(6) + ' values', 
                                        children = [
                                            html.Summary(str(6) + ' values'), 
                                            html.Table(children = 
                                                [
                                                    html.Tr(html.Td('1'.strip())),
                                                    html.Tr(html.Td('2'.strip())),
                                                    html.Tr(html.Td('3'.strip())),
                                                    html.Tr(html.Td('4'.strip())),
                                                    html.Tr(html.Td('5'.strip())),
                                                    html.Tr(html.Td('6'.strip()))
                                                ]
                                            )
                                        ]
                                    ))], style={'background-color': 'rgb(0,0,0)'}), 
                            None))
        testCases.append(('1;2;3;4;?5;6', 'data', 2,  
                          html.Tr(children=[html.Td(html.B('data'.replace('_', ' ').title())),
                                    html.Td(html.Details(title = str(6) + ' values', 
                                        children = [
                                            html.Summary(str(6) + ' values'), 
                                            html.Table(children = 
                                                [
                                                    html.Tr(html.Td('1'.strip())),
                                                    html.Tr(html.Td('2'.strip())),
                                                    html.Tr(html.Td('3'.strip())),
                                                    html.Tr(html.Td('4'.strip())),
                                                    html.Tr(html.Td(html.A('?5'[1:], href = '?5'[1:].strip(), target = '_blank'))),
                                                    html.Tr(html.Td('6'.strip()))
                                                ]
                                            )
                                        ]
                                    ))], style={'background-color': 'rgb(0,0,0)'}), 
                            None))
        falseCases = []
        falseCases.append(('1;2;3;4;?5;', 'data', 2,  
                          html.Tr(children=[html.Td(html.B('data'.replace('_', ' ').title())),
                                    html.Td(html.Details(title = str(6) + ' values', 
                                        children = [
                                            html.Summary(str(6) + ' values'), 
                                            html.Table(children = 
                                                [
                                                    html.Tr(html.Td('1'.strip())),
                                                    html.Tr(html.Td('2'.strip())),
                                                    html.Tr(html.Td('3'.strip())),
                                                    html.Tr(html.Td('4'.strip())),
                                                    html.Tr(html.Td(html.A('?5'[1:], href = '?5'[1:].strip(), target = '_blank'))),
                                                    html.Tr(html.Td('6'.strip()))
                                                ]
                                            )
                                        ]
                                    ))], style={'background-color': 'rgb(0,0,0)'}), 
                            None))                          
        for i in testCases:
            db.subTables = i[4]
            db.tableColors = tableColors
            self.assertEqual(db.createDetailRow(i[0], i[1], i[2]), i[3])
        for i in falseCases:
            db.subTables = i[4]
            db.tableColors = tableColors
            self.assertIsNot(db.createDetailRow(i[0], i[1], i[2]), i[3])

    def testCalculateEvents(self):
        testCases = []
        # Single event
        # chromStart, chromEnd, score, eventXValues, eventWidths, eventBases, eventScores, intervals, maxStack
        caseInput = ('test',0, 10, 0.5, {}, {}, {}, {}, [], 0)
        caseOutput = ({'test' : [4.5]}, {'test' : [10]}, {'test' : [0]}, {'test' : [0.5]}, [((0,10),0)], 1)
        testCases.append((caseInput, caseOutput))
        # Events overlapping
        # chromStart, chromEnd, score, eventXValues, eventWidths, eventBases, eventScores, intervals, maxStack
        caseInput = ('test', 0, 10, 0.5, {'test' : [4.5]}, {'test' : [10]}, {'test' : [0]}, {'test' : [0.5]}, [((0,10),0)], 1)
        caseOutput = ({'test' : [4.5,4.5]}, {'test' : [10,10]}, {'test' : [0,1.5]}, {'test' : [0.5,0.5]}, [((0,10),0),((0,10),1)], 2)
        testCases.append((caseInput, caseOutput))
        # Event bordering on right
        # chromStart, chromEnd, score, eventXValues, eventWidths, eventBases, eventScores, intervals, maxStack
        caseInput = ('test', 10, 15, 0.5, {'test' : [4.5]}, {'test' : [10]}, {'test' : [0]}, {'test' : [0.5]}, [((0,10),0)], 1)
        caseOutput = ({'test' : [4.5,12.0]}, {'test' : [10,5]}, {'test' : [0,0]}, {'test' : [0.5,0.5]}, [((0,10),0),((10,15),0)], 1)
        testCases.append((caseInput, caseOutput))
        # Event bordering on left
        # chromStart, chromEnd, score, eventXValues, eventWidths, eventBases, eventScores, intervals, maxStack
        caseInput = ('test', 0, 5, 0.5, {'test' : [7]}, {'test' : [5]}, {'test' : [0]}, {'test' : [0.5]}, [((5,10),0)], 1)
        caseOutput = ({'test' : [7,2]}, {'test' : [5,5]}, {'test' : [0,0]}, {'test' : [0.5,0.5]}, [((5,10),0),((0,5),0)], 1)
        testCases.append((caseInput, caseOutput))
        for i in testCases:
            xVals = i[0][4]
            widths = i[0][5]
            bases = i[0][6]
            scores = i[0][7]
            intervals = i[0][8]
            overlap = db.calculateEvents(i[0][0], i[0][1], i[0][2],
                            i[0][3], i[0][4], i[0][5], i[0][6], i[0][7], i[0][8], i[0][9])
            self.assertEqual((xVals, widths, bases, scores, intervals, overlap), i[1])

    def testCalculateEventsScoreColored(self):
        testCases = []
        # Single event
        # chromStart, chromEnd, score, eventXValues, eventWidths, eventBases, eventScores, intervals, maxStack
        caseInput = (0, 10, 0.5, [], [], [], [], [], 0)
        caseOutput = ([4.5], [10], [0], [0.5], [((0,10),0)], 1)
        testCases.append((caseInput, caseOutput))
        # Events overlapping
        # chromStart, chromEnd, score, eventXValues, eventWidths, eventBases, eventScores, intervals, maxStack
        caseInput = (0, 10, 0.5, [4.5], [10], [0], [0.5], [((0,10),0)], 1)
        caseOutput = ([4.5,4.5], [10,10], [0,1.5], [0.5,0.5], [((0,10),0),((0,10),1)], 2)
        testCases.append((caseInput, caseOutput))
        # Event bordering on right
        # chromStart, chromEnd, score, eventXValues, eventWidths, eventBases, eventScores, intervals, maxStack
        caseInput = (10, 15, 0.5, [4.5], [10], [0], [0.5], [((0,10),0)], 1)
        caseOutput = ([4.5,12.0], [10,5], [0,0], [0.5,0.5], [((0,10),0),((10,15),0)], 1)
        testCases.append((caseInput, caseOutput))
        # Event bordering on left
        # chromStart, chromEnd, score, eventXValues, eventWidths, eventBases, eventScores, intervals, maxStack
        caseInput = (0, 5, 0.5, [7], [5], [0], [0.5], [((5,10),0)], 1)
        caseOutput = ([7,2], [5,5], [0,0], [0.5,0.5], [((5,10),0),((0,5),0)], 1)
        testCases.append((caseInput, caseOutput))
        for i in testCases:
            xVals = i[0][3]
            widths = i[0][4]
            bases = i[0][5]
            scores = i[0][6]
            intervals = i[0][7]
            overlap = db.calculateEventsScoreColored(i[0][0], i[0][1],
                            i[0][2], i[0][3], i[0][4], i[0][5], i[0][6], i[0][7], i[0][8])
            self.assertEqual((xVals, widths, bases, scores, intervals, overlap), i[1])
    
#    def testSetUpBlockConstraints(self):
#        testCases = []
#        
#       # caseInput = (23311, 24099, "0","788", 23311, 24099)
#    #    # blockStartsF, blockSizesF
#   ##     caseOutput = ([200,280,-1], [40,20,40])
#    #    testCases.append((caseInput, caseOutput))
#        
#        # Test overlap on right side of region and with chromStart/end equal xAxisMin/Max
#        # chromStart, chromEnd, blockStarts, blockSizes, xAxisMin, xAxisMax
#        caseInput = (0, 300, "200,280,340","40,40,40", 0, 300)
#        # blockStartsF, blockSizesF
#        caseOutput = ([200,280,-1], [40,20,40])
#        testCases.append((caseInput, caseOutput))
#        
#        # Test overlap on right side of region
#        # chromStart, chromEnd, blockStarts, blockSizes, xAxisMin, xAxisMax
#        caseInput = (100, 400, "100,180,240","40,40,40", 100, 300)
#        # blockStartsF, blockSizesF
#        caseOutput = ([200,280,-1], [40,20,40])
#        testCases.append((caseInput, caseOutput))
#        
#        # Test overlap on left side of region
#        # chromStart, chromEnd, blockStarts, blockSizes, xAxisMin, xAxisMax
#        caseInput = (0, 200, "40,80,140","40,40,40", 100, 300)
#        # blockStartsF, blockSizesF
#        caseOutput = ([-1,100,140], [40,20,40])
#        testCases.append((caseInput, caseOutput))
#        
#        # Test extension over both sides of the region
#        # chromStart, chromEnd, blockStarts, blockSizes, xAxisMin, xAxisMax
#        caseInput = (0, 500, "40,80,240,400","40,40,70,40", 100, 300)
#        # blockStartsF, blockSizesF
#        caseOutput = ([-1,100,240,-1], [40,20,60,40])
#        testCases.append((caseInput, caseOutput))
#        
#        # Test inclusion in region
#        # chromStart, chromEnd, blockStarts, blockSizes, xAxisMin, xAxisMax
#        caseInput = (120, 200, "40,80","40,40", 100, 300)
#        # blockStartsF, blockSizesF
#        caseOutput = ([160, 200], [40, 40])
#        testCases.append((caseInput, caseOutput))       
#        for i in testCases:
#            self.assertEquals(db.setUpBlockConstraints(i[0][0],i[0][1],i[0][2],i[0][3],i[0][4],i[0][5]), i[1])
    
    def testCalculateBlocks(self):
        testCases = []
        
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (23311,24099, 23311, 24099, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([29.5],[0.4],[20])
        testCases.append((caseInput,caseOutput))
        
        # BLock lies completely in coding region
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (0,100, 20, 40, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([29.5],[0.4],[20])
        testCases.append((caseInput,caseOutput))
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (0,100, 21, 40, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([30],[0.4],[19])
        testCases.append((caseInput,caseOutput))
        
        # Block lies right of coding region
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (0,10, 20, 40, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([30],[0.2],[21])
        testCases.append((caseInput,caseOutput))
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (0,10, 21, 41, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([31],[0.2],[21])
        testCases.append((caseInput,caseOutput))
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (0,10, 21, 40, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([30.5],[0.2],[20])
        testCases.append((caseInput,caseOutput))
        
        # Block lies left of coding region
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (20,30, 0, 10, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([4.5],[0.2],[10])
        testCases.append((caseInput,caseOutput))
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (20,30, 0, 11, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([5],[0.2],[11])
        testCases.append((caseInput,caseOutput))
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (20,30, 1, 11, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([5.5],[0.2],[10])
        testCases.append((caseInput,caseOutput))
        
        # Block overlaps coding region on the left
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (0,10, 5, 15, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([7,12],[0.4,0.2],[5,5])
        testCases.append((caseInput,caseOutput))
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (0,10, 6, 15, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([7.5,12],[0.4,0.2],[4,5])
        testCases.append((caseInput,caseOutput))
         # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (0,10, 6, 16, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([7.5,12.5],[0.4,0.2],[4,6])
        testCases.append((caseInput,caseOutput))
        
        # Block overlaps coding region on the right
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (5,15, 0, 10, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([2,7],[0.2,0.4],[5,5])
        testCases.append((caseInput,caseOutput))
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (5,15, 1, 10, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([2.5,7],[0.2,0.4],[4,5])
        testCases.append((caseInput,caseOutput))
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (5,15, 1, 9, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([2.5,6.5],[0.2,0.4],[4,4])
        testCases.append((caseInput,caseOutput))
        
        # Block completely contains coding region
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (5,15, 1, 11, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([2.5,7.5],[0.2,0.4],[4,6])
        testCases.append((caseInput,caseOutput))
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (5,15, 5, 15, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([9.5],[0.4],[10])
        testCases.append((caseInput,caseOutput))
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (5,16, 5, 16, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([10],[0.4],[11])
        testCases.append((caseInput,caseOutput))
        
        # Block has 0 size
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (5,15, 1, 1, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([],[],[])
        testCases.append((caseInput,caseOutput))
        for i in testCases:
            inputBlockVals = []
            inputBlockYs = []
            inputBlockWidths = []
            db.calculateBlocks(i[0][0],i[0][1],i[0][2],i[0][3], inputBlockVals, inputBlockWidths, inputBlockYs, i[0][4])
            output = (inputBlockVals, inputBlockYs, inputBlockWidths)
            self.assertEquals(output, i[1])
            
if __name__ == '__main__':
    unittest.main()