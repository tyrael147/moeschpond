import pandas as pd
import bw2data as bd
import bw2calc as bc
import bw2io as bi
import bw_processing as bwp
import numpy as np
from pathlib import Path

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


def modify_w_arrays(data_object,new_arrays):
    n = 1
    for k,v in new_arrays.items():
        n = len(v)        

    data, _ = data_object.get_resource(f"{data_object.metadata['name']}_technosphere_matrix.data")
    indices, _ = data_object.get_resource(f"{data_object.metadata['name']}_technosphere_matrix.indices")
    flip, _ = data_object.get_resource(f"{data_object.metadata['name']}_technosphere_matrix.flip")
    dp_dict = dict(
        zip(indices.astype("object"),[[tup[0], tup[1]] for tup in zip(data,flip)])
                        )
    for key, value in new_arrays.items():
        dp_dict[key][0] = value
    
    new_foreground = bwp.create_datapackage(
    fs = bwp.generic_zipfile_filesystem(dirpath=Path("./data/inputs"), filename=f"{data_object.metadata['name']}.zip", write=True),
    # combinatorial=True,
    sequential=True,
    )

    for row_col, data_flip in dp_dict.items():
        if not isinstance(data_flip[0], np.ndarray):
            new_array = np.full((n,), fill_value = data_flip[0])
            dp_dict[row_col][0] = new_array
            
    new_data = np.array([val[0] for val in dp_dict.items()])
                   
    new_foreground.add_persistent_array(
    matrix="technosphere_matrix",
    data_array=new_data,
    indices_array=indices.astype(bwp.INDICES_DTYPE),
    flip_array=flip,
    name=data_object.metadata['name'],
)

    # return dp_dict
    return new_foreground
    