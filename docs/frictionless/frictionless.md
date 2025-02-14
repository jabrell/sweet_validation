# Frictionless Data

## Overview

We use the [Frictionless Data standard](https://datapackage.org/)
to describe data. In short the frictionless standard relies on to four main components:

1. **Table schema** provides a section to describe a table, i.e., a meta-data section
    and describes the table schema in terms of fields.
2. **Table dialect** provides the possibility to describe the physical properties
    of a table, i.e, how data are stored in a file.
3. **Data resource** is the combination of a datafile and the respective descriptions
    given in the form of table schemas and dialects.
4. **Data package** allows to bundle several data resources.

Our package relies on table schemas to describe data and we therefore explain their
concept in greater detail.

## Table Schema

A frictionless table schema is a [json-schema](https://tour.json-schema.org/)
specification to standardize the exchange of data. For all details take a look at
the [specification of the table schema](https://datapackage.org/profiles/2.0/dataresource.json).
Our approach uses yaml files to describe data. Consider the following example of
such a yaml:

```yaml
name: generation
title: Electricity generation
description: >
    Electricity generation created by our awesome very unique electricity model
    that is technically and economically very advanced. The table provides
    annual generation by technology and year.
created_by: User
created_at: 2025-01-31
fields:
  - name: technology
    type: string
    constraint:
        required: true
        enum: [gas, coal, wind, solar]
  - name: year
    type: integer
    constraint:
        required: true
        minimum: 2000
        maximum: 2100
  - name: value
    type: number
    constrain:
        required: true
```

The table schema comes in two parts. The first part are the meta-data that describe
the data and provides additional information, e.g., operational meta-data who
created the data and at which date. The description of relational constrains including
primary and foreign keys is also possible. It is possible to add any field you want
to the meta-data section.

The *fields* part describes the columns of the data. *fields* are by default the only
part that is mandatory. A *field* has to have a name and should have at least a
type, i.e, whether you are storing strings, numbers, integer, ... (see description
of [all possible types](https://framework.frictionlessdata.io/docs/fields/any.html)).
Fields can be narrowed down using [constraints](https://specs.frictionlessdata.io/table-schema/#constraints):
- required: Whether the field must be given
- unique: Whether values in the field must be unique
- minLength/maxLength: Allows to set the minimal and maximum value for collections
(arrays, lists, strings)
- maximum/minimum: Maximum/minimum for numerical values
- pattern: Restrict strings by regular expressions
- enum: Define a list of valid values for a string

<!-- ## Meta-data restrictions

The table schema describes a table and its columns. While that is sufficient to
describe data, it does not allow to standardize the description of the tables, i.e.,
the meta-data. To allow for the standardization of meta-data we use table schema
that describes the meta-data:

```yaml
name: metadata_schema
description: |
  Description of the metadata standard. The metadata section of all resource
  description must comply

fields:
  - name: name
    type: string
    constraints:
      required: true
  - name: description
    type: string
    constraints:
      required: true
  - name: created_by
    type: string
    constraints:
      required: true
  - name: tags
    type: array
    items:
      type: string
```

The schema above describes the meta-data of table resources and defines an additional
field *tags* to be used to make the data searchable. The field is not required, so the
generation schema above would comply with the standard. Version 1 of Frictionless,
does not allow to restrict the table to match exactly the fields stated, i.e., it is
possible to add additional fields. This is why the generation schema complies although
it adds the field *title* to the meta-data. -->
