from sfepy.base.base import import_file, get_default, OneTypeList
from sfepy.base.conf import ProblemConf
from sfepy.discrete.problem import Problem
from sfepy.discrete.functions import Functions
from sfepy.discrete.fem.mesh import Mesh
from sfepy.discrete.fem.domain import FEDomain
from sfepy.discrete.common.region import (Region, get_dependency_graph,
                                          sort_by_dependency, get_parents)
from sfepy.discrete.parse_regions import create_bnf, visit_stack, ParseException


filename = r"C:\Users\Benjamin\Desktop\stage 2023\disque_3d.py"
funmod_ = import_file(filename, package_name=False)

define_dict = funmod_.__dict__

conf_ = ProblemConf(define_dict, funmod_)

functions_ = Functions.from_conf(conf_.functions)



mesh = Mesh.from_file(conf_.filename_mesh)
domain_ = FEDomain(mesh.name, mesh)

obj_ = Problem('problem_from_conf', conf=conf_, functions=functions_, domain=domain_, auto_conf=False, active_only=True)



# conf.regions = {'region_Omega__0': Struct:Omega, 'region_circonference__1': Struct:circonference, 
#                    'region_center_0__2': Struct:center_0, 'region_supported__3': Struct:supported}

# obj.functions = 
#    Functions
#     _objs:
#       list: [
#         Function:select_circ_out
#           extra_args:
#             dict with keys: []
#           function:
#             <function <lambda> at 0x0000027A4FA47B80>
#           is_constant:
#             False
#           name:
#             select_circ_out
#         Function:select_circ_in
#           extra_args:
#             dict with keys: []
#           function:
#             <function <lambda> at 0x0000027A600E5C10>
#           is_constant:
#             False
#           name:
#             select_circ_in
#         Function:select_supports
#           extra_args:
#             dict with keys: []
#           function:
#             <function <lambda> at 0x0000027A600E5CA0>
#           is_constant:
#             False
#           name:
#             select_supports
#       ]
#     names:
#       list: ['select_circ_out', 'select_circ_in', 'select_supports']






# obj.set_regions(conf.regions, obj.functions, allow_empty=allow_empty)


def set_regions(self, conf_regions=None, conf_materials=None, functions=None, allow_empty=False):  #class Problem
  
  
    conf_regions = get_default(conf_regions, self.conf.regions)
    functions = get_default(functions, self.functions)

    self.domain.create_regions(conf_regions, functions, allow_empty=allow_empty)
    

        
conf_regions = get_default(conf_.regions, obj_.conf.regions)
functions = get_default(obj_.functions, obj_.functions)



