from graph_db.configuration import Configuration, makeAttribute, makeAllowedRelation


class TestConstructor(Configuration):
    def __init__(self):
        Configuration.__init__(self)

        ############ NODES #############
        base_attributes_top = [
            makeAttribute("readable_name", "Readable Name", "For rapid people understanding", self.TYPE_STRING, ""),
            makeAttribute("name", "Unique API Name", "For automated scripts, should be permanent", self.TYPE_STRING, ""),
            ]
        base_attributes_bottom = [
            makeAttribute("description", "Description", "For people some additional information", self.TYPE_TEXT, ""),
            ]

        # addEntityClass(cid, name, readable_name, description, attributes_list)
        # basic type classes
        self.addEntityClass(1, "object_type", "Object type", "", base_attributes_top + base_attributes_bottom)

        self.addEntityClass(2, "pin_type", "Pin type", "", base_attributes_top + base_attributes_bottom)

        self.addEntityClass(3, "socket_type", "Socket type", "", base_attributes_top + [
                makeAttribute("direction", "Links direction", "in or out or none", self.TYPE_STRING, ""),
            ] + base_attributes_bottom)

        self.addEntityClass(4, "link_type", "Link type", "", base_attributes_top + base_attributes_bottom)

        # templates
        self.addEntityClass(5, "template", "Template", "", base_attributes_top + base_attributes_bottom)

        self.addEntityClass(6, "template_socket", "Template Socket", "", base_attributes_top + [
            ] + base_attributes_bottom)
        
        # instances
        self.addEntityClass(7, "object", "Object", "", base_attributes_top + base_attributes_bottom)

        self.addEntityClass(8, "pin", "Pin", "", base_attributes_top + base_attributes_bottom)

        self.addEntityClass(9, "socket", "Socket", "",  base_attributes_top + [
            ] + base_attributes_bottom)
        
        self.addEntityClass(10, "link", "Link", "",  base_attributes_top + [
            ] + base_attributes_bottom)
        
        # view attributes
        self.addEntityClass(11, "view", "View", "",  base_attributes_top + [
            ] + base_attributes_bottom)
        
        self.addEntityClass(12, "coords", "Coordinates", "",  base_attributes_top + [
                makeAttribute("x", "x", "X coordinate on view", self.TYPE_DOUBLE, ""),
                makeAttribute("y", "y", "Y coordinate on view", self.TYPE_DOUBLE, ""),
            ] + base_attributes_bottom)
        
        self.addEntityClass(13, "display_attrs", "Display Attributes", "",  base_attributes_top + [
                makeAttribute("shape", "Shape", "Circle, Square or something else", self.TYPE_STRING, ""),
                makeAttribute("color", "Color", "#ffffff", self.TYPE_STRING, ""),
                makeAttribute("size", "Size", "Should be > 0", self.TYPE_INTEGER, ""),
                makeAttribute("image", "Image", "Should be an url", self.TYPE_STRING, ""),
                makeAttribute("scale", "Scale", "Should be > 0", self.TYPE_DOUBLE, ""),
            ] + base_attributes_bottom)
        
        # tag class
        self.addEntityClass(149, "tag", "tag", "",   base_attributes_top + [
            ])

        ############ EDGES #############
        self.addRelationClass(102, "instanceof", "Instance of", "Instance of type", [
        ], [
            makeAllowedRelation(
                {"cname":"template", "multiplicity" : self.MUL_ZERO_OR_MORE},
                {"cname":"object_type", "multiplicity" : self.MUL_ONE}
            ),
            makeAllowedRelation(
                {"cname":"object", "multiplicity" : self.MUL_ZERO_OR_MORE},
                {"cname":"template", "multiplicity" : self.MUL_ONE}
            ),
            makeAllowedRelation(
                {"cname":"pin", "multiplicity" : self.MUL_ZERO_OR_MORE},
                {"cname":"pin_type", "multiplicity" : self.MUL_ONE}
            ),
            makeAllowedRelation(
                {"cname":"template_socket", "multiplicity" : self.MUL_ZERO_OR_MORE},
                {"cname":"socket_type", "multiplicity" : self.MUL_ONE}
            ),
            makeAllowedRelation(
                {"cname":"socket", "multiplicity" : self.MUL_ZERO_OR_MORE},
                {"cname":"template_socket", "multiplicity" : self.MUL_ONE}
            ),
            makeAllowedRelation(
                {"cname":"link", "multiplicity" : self.MUL_ZERO_OR_MORE},
                {"cname":"link_type", "multiplicity" : self.MUL_ONE}
            ),
            ])

        self.addRelationClass(103, "composition", "Composition", "Composition links", [
        ], [
            makeAllowedRelation(
                {"cname":"object_type", "multiplicity" : self.MUL_ONE},
                {"cname":"pin", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            makeAllowedRelation(
                {"cname":"socket_type", "multiplicity" : self.MUL_ONE},
                {"cname":"pin_type", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            makeAllowedRelation(
                {"cname":"template_socket", "multiplicity" : self.MUL_ONE},
                {"cname":"pin", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            makeAllowedRelation(
                {"cname":"template", "multiplicity" : self.MUL_ONE},
                {"cname":"template_socket", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            makeAllowedRelation(
                {"cname":"object", "multiplicity" : self.MUL_ONE},
                {"cname":"socket", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            ])

        self.addRelationClass(104, "attributes", "Attributes", "Additional attribute instance", [
        ], [
            makeAllowedRelation(
                {"cname":"object", "multiplicity" : self.MUL_ONE},
                {"cname":"coords", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            makeAllowedRelation(
                {"cname":"template_socket", "multiplicity" : self.MUL_ONE},
                {"cname":"coords", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            makeAllowedRelation(
                {"cname":"socket_type", "multiplicity" : self.MUL_ONE},
                {"cname":"display_attrs", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            makeAllowedRelation(
                {"cname":"template", "multiplicity" : self.MUL_ONE},
                {"cname":"display_attrs", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
        ])
        
        self.addRelationClass(105, "logical", "Logical", "Logical connections", base_attributes_top+[
        ], [
            makeAllowedRelation(
                {"cname":"coords", "multiplicity" : self.MUL_ZERO_OR_MORE},
                {"cname":"view", "multiplicity" : self.MUL_ONE}
            ),
            makeAllowedRelation(
                {"cname":"display_attrs", "multiplicity" : self.MUL_ZERO_OR_MORE},
                {"cname":"view", "multiplicity" : self.MUL_ONE}
            ),
       ])
        
        self.addRelationClass(106, "connectable", "Connectable", "Connection is allowed", base_attributes_top+[
        ], [
            makeAllowedRelation(
                {"cname":"pin_type", "multiplicity" : self.MUL_ZERO_OR_MORE},
                {"cname":"pin_type", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
       ])
        
        self.addRelationClass(107, "from_link", "From Link", "Link connection: from_socket", base_attributes_top+[
        ], [
            makeAllowedRelation(
                {"cname":"link_type", "multiplicity" : self.MUL_ONE},
                {"cname":"socket_type", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            makeAllowedRelation(
                {"cname":"link", "multiplicity" : self.MUL_ONE},
                {"cname":"socket", "multiplicity" : self.MUL_ZERO_OR_ONE}
            ),
       ])
        
        self.addRelationClass(108, "to_link", "To Link", "Link connection: to_socket", base_attributes_top+[
        ], [
            makeAllowedRelation(
                {"cname":"link_type", "multiplicity" : self.MUL_ONE},
                {"cname":"socket_type", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            makeAllowedRelation(
                {"cname":"link", "multiplicity" : self.MUL_ONE},
                {"cname":"socket", "multiplicity" : self.MUL_ZERO_OR_ONE}
            ),
       ])
        
        self.addRelationClass(1149, "tag_link", "tag_link", "Tag link", [
        ], [
            makeAllowedRelation(
                {"cname":"object", "multiplicity" : self.MUL_ZERO_OR_MORE},
                {"cname":"tag", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
        ])

