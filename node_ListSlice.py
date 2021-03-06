import bpy
from node_s import *
from util import *

# ListSlice
# by Linus Yng

# utility generator function for use instead of fullList when input does not match,
# note, non terminating process.
# to move to util

def repeat_last(lst):
    i = -1
    while True:
        i += 1
        if len(lst) > i:
            yield lst[i]
        else:
            yield lst[-1]
            

# Slices a list using function like:
# Slice  = data[start:stop]
# Other = data[:start]+data[stop:]
       
class ListSliceNode(Node, SverchCustomTreeNode):
    ''' List Slice '''
    bl_idname = 'ListSliceNode'
    bl_label = 'List Slice'
    bl_icon = 'OUTLINER_OB_EMPTY'
    
    level = bpy.props.IntProperty(name = 'level_to_count', default=2, min=1, update=updateNode)
    start = bpy.props.IntProperty(name = 'start', default=0, update=updateNode)
    stop = bpy.props.IntProperty(name = 'stop', default=1, update=updateNode)

    typ = bpy.props.StringProperty(name='typ', default='')
    newsock = bpy.props.BoolProperty(name='newsock', default=False)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "level", text="level")
        layout.prop(self, "start", text="Start")
        layout.prop(self, "stop", text="Stop")
        
    def init(self, context):
        self.inputs.new('StringsSocket', "Data", "Data")
        self.inputs.new('StringsSocket', "Start", "Start")
        self.inputs.new('StringsSocket', "Stop", "Stop")
        self.outputs.new('StringsSocket',"Slice","Slice")
        self.outputs.new('StringsSocket',"Other","Other")

    def update(self):
        if 'Data' in self.inputs and len(self.inputs['Data'].links)>0:
            inputsocketname = 'Data'
            outputsocketname = ['Slice','Other']
            changable_sockets(self, inputsocketname, outputsocketname)
        
        if 'Slice' in self.outputs and self.outputs['Slice'].links or \
                'Other' in self.outputs and self.outputs['Other'].links:
            
            if 'Data' in self.inputs and self.inputs['Data'].links:
                data = SvGetSocketAnyType(self, self.inputs['Data'])
                
                if 'Start' in self.inputs and self.inputs['Start'].is_linked:
                    start = SvGetSocketAnyType(self,self.inputs['Start'])[0]
                else:
                    start = [self.start]
                
                if 'Stop' in self.inputs and self.inputs['Stop'].is_linked:
                    stop = SvGetSocketAnyType(self,self.inputs['Stop'])[0]
                else:
                    stop = [self.stop]
                    
                if 'Slice' in self.outputs and self.outputs['Slice'].links:
                    out = self.get(data,start,stop,self.level,self.slice)
                    SvSetSocketAnyType(self, 'Slice', out)
                if 'Other' in self.outputs and self.outputs['Other'].links:
                    out = self.get(data, start,stop,self.level,self.other)
                    SvSetSocketAnyType(self, 'Other', out)
    
    def slice(self,data,start,stop):
        if type(data) in [tuple,list]:
            return data[start:stop]
        else:
            return None
            
    def other(self,data,start,stop):
        if type(data) in [tuple,list]:
            return data[:start]+data[stop:]
        else:
            return None
            
    def get(self,data, start, stop, level, f):
        if level>1: # find level to work on
            return [self.get(obj,start,stop,level-1,f) for obj in data]
        elif level==1: #execute the chosen function
            start_iter = repeat_last(start)
            stop_iter = repeat_last(stop)
            return [f(obj,next(start_iter),next(stop_iter)) for obj in data]
        else: #Fail
            return None
        
    def update_socket(self, context):
        self.update()

def register():
    bpy.utils.register_class(ListSliceNode)   
    
def unregister():
    bpy.utils.unregister_class(ListSliceNode)


if __name__ == "__main__":
    register()