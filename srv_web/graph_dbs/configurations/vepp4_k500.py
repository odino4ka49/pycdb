from graph_db.configuration import Configuration, makeAttribute, makeAllowedRelation


class VEPP4K500(Configuration):
    def __init__(self):
        Configuration.__init__(self)

        ############ NODES #############
        base_attributes_top = [
            makeAttribute("readable_name", "Readable Name", "For rapid people understanding", self.TYPE_STRING, ""),
            makeAttribute("name", "Unique API Name", "For automated scripts, should be permanent", self.TYPE_STRING, ""),
            ]
        base_attributes_bottom = [
            makeAttribute("note", "Note", "For people, for example, some errors history notes", self.TYPE_TEXT, ""),
            ]

        # addEntityClass(cid, name, readable_name, description, attributes_list)
        self.addEntityClass(1, "server", "Server", "", base_attributes_top + [
            makeAttribute("address", "IP or Domain Name", "", self.TYPE_STRING, "0.0.0.0"),
            ] + base_attributes_bottom)

        self.addEntityClass(2, "ioc", "IOC", "", base_attributes_top + [
            makeAttribute("template", "Template", "Template file for generating IOC's config", self.TYPE_STRING, "ioc.tmpl"),
            ] + base_attributes_bottom)

        self.addEntityClass(3, "device", "Device", "", base_attributes_top + [
            makeAttribute("params", "Parameters", "A set of device parameters", self.TYPE_DICTIONARY, {}),
            ] + base_attributes_bottom)

        self.addEntityClass(4, "device_type", "Device Type", "", base_attributes_top + [
            makeAttribute("params", "Parameters", "A set of device type parameters", self.TYPE_DICTIONARY, {"PSy" : "BR"}),
            makeAttribute("template", "Template", "Template dir name to use for generating IOC's config", self.TYPE_STRING, ""),
            ] + base_attributes_bottom)

        self.addEntityClass(5, "cs_channel", "CS Channel", "", base_attributes_top + [
            makeAttribute("default_value", "Default Value", "Default value of the channel", self.TYPE_DOUBLE, 0.0),
            ] + base_attributes_bottom)

        self.addEntityClass(6, "logical_pin", "Logical Pin", "", base_attributes_top + [
            ] + base_attributes_bottom)

        # Tiny class without base attributes
        self.addEntityClass(7, "logical_socket", "Logical Socket", "", base_attributes_top + [
            ] + base_attributes_bottom)

        self.addEntityClass(8, "logical_socket_type", "Logical Socket Type", "", base_attributes_top + [
            ] + base_attributes_bottom)

        # Tiny class without base attributes
        self.addEntityClass(9, "device_profile", "Device Profile", "",  base_attributes_top + [
            ] + base_attributes_bottom)

        ############ EDGES #############
        self.addRelationClass(102, "type", "Types", "Typification links", [
        ], [
            makeAllowedRelation(
                {"cname":"device", "multiplicity" : self.MUL_ZERO_OR_MORE},
                {"cname":"device_type", "multiplicity" : self.MUL_ONE}
            ),
            makeAllowedRelation(
                {"cname":"logical_socket", "multiplicity" : self.MUL_ZERO_OR_MORE},
                {"cname":"logical_socket_type", "multiplicity" : self.MUL_ONE}
            ),
            ])

        self.addRelationClass(103, "composition", "Compositions", "Compositions links", [
        ], [
            makeAllowedRelation(
                {"cname":"device", "multiplicity" : self.MUL_ONE},
                {"cname":"logical_socket", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            makeAllowedRelation(
                {"cname":"device_type", "multiplicity" : self.MUL_ONE},
                {"cname":"cs_channel", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            makeAllowedRelation(
                {"cname":"device_type", "multiplicity" : self.MUL_ONE},
                {"cname":"logical_pin", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            makeAllowedRelation(
                {"cname":"device_profile", "multiplicity" : self.MUL_ONE},
                {"cname":"logical_socket_type", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            ])

        self.addRelationClass(104, "logical", "Logical", "Logical connections", [
        ], [
            makeAllowedRelation(
                {"cname":"server", "multiplicity" : self.MUL_ONE},
                {"cname":"ioc", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            makeAllowedRelation(
                {"cname":"ioc", "multiplicity" : self.MUL_ONE},
                {"cname":"device", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),

            # Dev-Connection-Dev
            makeAllowedRelation(
                {"cname":"device", "multiplicity" : self.MUL_ONE},
                {"cname":"device", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            makeAllowedRelation(
                {"cname":"device", "multiplicity" : self.MUL_ONE},
                {"cname":"device_profile", "multiplicity" : self.MUL_ONE}
            ),

            # DevT-ConnectionT-DevT
            makeAllowedRelation(
                {"cname":"device_type", "multiplicity" : self.MUL_ONE},
                {"cname":"device_profile", "multiplicity" : self.MUL_ZERO_OR_MORE}
            ),
            makeAllowedRelation(
                {"cname":"logical_pin", "multiplicity" : self.MUL_ZERO_OR_ONE},
                {"cname":"logical_socket_type", "multiplicity" : self.MUL_ONE}
            ),

            makeAllowedRelation(
                {"cname":"logical_socket", "multiplicity" : self.MUL_ONE},
                {"cname":"logical_socket", "multiplicity" : self.MUL_ONE}
            ),
        ])
        
        self.addRelationClass(105, "logical", "Logical", "Logical connections", base_attributes_top+[
        ], [
            makeAllowedRelation(
                {"cname":"logical_pin", "multiplicity" : self.MUL_ZERO_OR_MORE},
                {"cname":"logical_socket_type", "multiplicity" : self.MUL_ONE}
            ),
       ])

