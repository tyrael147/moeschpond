import pandas as pd
import bw2data as bd
import bw2calc as bc
import bw2io as bi
import bw_processing as bwp
import numpy as np
from pathlib import Path

###templates
#############################################
# cf.new_edge(
#     amount=237.3,  # plus 58 kWh of electricity, in ecoinvent 3.8
#     uncertainty_type=5,
#     minimum=200,
#     maximum=300,
#     type='technosphere',
#     input=ng,
# ).save()
#############################################
# cf.new_edge(
#     amount=26.6,
#     uncertainty_type=5,
#     minimum=26,
#     maximum=27.2,
#     type='biosphere',
#     input=co2,
# ).save()
##################################################
# data = {
#     'code': 'cf',
#     'name': 'carbon fibre production',
#     'location': 'DE',
#     'unit': 'kg'
# }
#
# cf = db.new_node(**data)
# cf.save()
#
dict_metadata = {
    100000:{
        "name":"Production of example",
        "code":"Production of example".replace(" ","_"),
        "location":"CH",
        "unit":"kg"
    }
}
Data_Objects = list[bwp.Datapackage]
def database_creator(db_name:str="default_new", data_objs: Data_Objects = None, dict_metadata=None):

    # Creates new empty db
    if db_name in bd.databases:
        del bd.databases[db_name]
    db = bd.Database(db_name)
    db.write({})
    indices = None
    data = None
    flip = None
    unique_indices = []
    for object in data_objs:

        for resource in object.resources:
            if resource["matrix"] == "technosphere_matrix" and resource["kind"]=="indices":
                indices,_ = object.get_resource(resource["name"])
                unique_indices = set([a for b in indices for a in b])
            if resource["matrix"] == "technosphere_matrix" and resource["kind"]=="data":
                data,_ = object.get_resource(resource["name"])
            if resource["matrix"] == "technosphere_matrix" and resource["kind"]=="flip":
                flip,_ = object.get_resource(resource["name"])

    stack_values = np.stack([indices.astype("object"), data, flip], axis=1)

    ## Creating non-existing nodes
    for id in unique_indices:
        if id in dict_metadata:
            node = db.new_node({
                    'code': dict_metadata[id]["code"],
                    'name': dict_metadata[id]["name"],
                    'location': dict_metadata[id]["location"],
                    'unit': dict_metadata[id]["unit"],
                    'id':id,
                })
            db.write(node)

    ## Creating edges