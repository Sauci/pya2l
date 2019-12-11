"""
@project: pya2l
@file: node.py
@author: Guillaume Sottas
@date: 28.12.2018
"""

from pya2l.parser.if_data_node import AmlDynNode, AmlDynStruct
from pya2l.shared import ASTNode, node_type


class A2MLNode(ASTNode):
    def get_class(self, tokens): raise NotImplementedError

    def dump(self, n=0): raise NotImplementedError(self.__class__.__name__)


class TypeName(A2MLNode):
    tagged_type_name = dict()
    __slots__ = 'identifier', 'is_def', 'node_type'

    def __init__(self, node_type, identifier=None, member=None):
        self.node_type = node_type
        self.identifier = None
        self.is_def = member is None
        if self.is_def:
            member = tuple()
        super(TypeName, self).__init__(identifier, *member)

    def __iter__(self):
        raise NotImplementedError(self.__class__.__name__)

    @property
    def tagged(self):
        return self.identifier in TypeName.tagged_type_name.keys()

    def get_class(self, tokens):
        return TypeName.tagged_type_name[self.identifier].get_class(tokens, recurse=True)

    def dump(self, n=0):
        if self.is_def:
            yield n, '{node_type} {identifier}'.format(node_type=self.node_type, identifier=self.identifier)
        else:
            tmp = '{node_type}'
            if self.identifier:
                tmp += ' {identifier}'
            tmp += ' {{'
            yield n, tmp.format(node_type=self.node_type, identifier=self.identifier)
            for member in self:
                for e in member.dump(n=n + 1):
                    yield e
            yield n, '}'


class A2ML(list):

    def __init__(self, *args, **kwargs):
        super(A2ML, self).__init__(*args, **kwargs)

    def get_class(self, tokens):
        for node in self:
            if isinstance(node.definition, TypeDefinition):
                # if the declaration is a type definition, register it the corresponding dictionary. this property won't
                # appear in the AST.
                TypeName.tagged_type_name[node.definition.type_name.identifier] = node.definition.type_name
            else:
                return node.definition.get_class(tokens)


@node_type('a2ml_declaration')
class Declaration(A2MLNode):
    __slots__ = 'definition',

    def __init__(self, definition):
        self.definition = None
        super(Declaration, self).__init__(definition)

    @property
    def tag(self):
        return self.definition.tag

    def get_class(self, tokens): return super(Declaration, self).get_class(tokens)

    def dump(self, n=0):
        d = list(self.definition.dump(n=n))
        d[-1] = (d[-1][0], d[-1][1] + ';')
        return (e for e in d)


@node_type('block')
class BlockDefinition(A2MLNode):
    __slots__ = 'tag', 'type_name'

    def __init__(self, tag, type_name):
        self.tag = None
        self.type_name = None
        super(BlockDefinition, self).__init__(tag, type_name)

    def get_class(self, tokens):
        if len(tokens):
            tag = tokens.pop(0)
            if tag == self.tag:
                obj = self.type_name.get_class(tokens)
            else:
                raise Exception()
        else:
            obj = None
        return obj

    def dump(self, n=0):
        yield n, 'block "{tag}"'.format(tag=self.tag)
        for e in self.type_name.dump(n=n):
            yield e


@node_type('a2ml_type_definition')
class TypeDefinition(A2MLNode):
    __slots__ = 'type_name',

    def __init__(self, type_name):
        self.type_name = None
        super(TypeDefinition, self).__init__(type_name)

    def get_class(self, tokens): return super(TypeDefinition, self).get_class(tokens)

    def dump(self, n=0):
        return (e for e in self.type_name.dump(n=n))


@node_type('int')
@node_type('long')
@node_type('uint')
@node_type('ulong')
@node_type('double')
@node_type('float')
class PredefinedTypeName(A2MLNode):
    __slots__ = 'type_name',

    def __init__(self, type_name):
        self.type_name = None
        super(PredefinedTypeName, self).__init__(type_name)

    @property
    def required(self):
        return True

    def get_class(self, tokens):
        return type('P', ({'char': int,
                           'int': int,
                           'long': int,
                           'uchar': int,
                           'uint': int,
                           'ulong': int,
                           'double': float,
                           'float': float}[self.type_name],), {})(tokens.pop(0))

    def dump(self, n=0):
        yield n, self.type_name


@node_type('char')
class Char(PredefinedTypeName):

    def get_class(self, tokens):
        token = tokens.pop(0)
        if isinstance(token, str):
            return type('P', (str,), {})(token)
        return type('P', (int,), {})(token)


@node_type('uchar')
class UChar(Char):
    pass


@node_type('a2ml_struct_type_name')
class Struct(TypeName):
    __slots__ = 'member',

    def __init__(self, identifier=None, member=None):
        self.member = list()
        super(Struct, self).__init__('struct', identifier, member)

    def __iter__(self):
        return (e for e in self.member)

    @property
    def required(self):
        return True

    def get_class(self, tokens, recurse=False):
        if self.tagged and not recurse:
            return super(Struct, self).get_class(tokens)
        else:
            args, kwargs = list(), dict()
            for node in self:
                obj = node.get_class(tokens)
                if node.required:
                    if isinstance(obj, AmlDynStruct):
                        for arg in obj.positionals():
                            args.append(arg)
                    else:
                        args.append(obj)
                else:
                    if isinstance(obj, AmlDynNode):
                        for k, v in obj.keywords():
                            kwargs[k] = v
                        for arg in obj.positionals():
                            args.append(arg)
                    else:
                        args.append(obj)
            return AmlDynStruct(args, kwargs)

    def dump(self, n=0):
        return super(Struct, self).dump(n=n)


@node_type('a2ml_struct_member')
class StructMember(A2MLNode):  # TODO: remove this class, as it only perform calls to 'member' property.
    __slots__ = 'member',

    def __init__(self, member):
        self.member = None
        super(StructMember, self).__init__(member)

    @property
    def required(self):
        return self.member.required

    def get_class(self, tokens):
        return self.member.get_class(tokens)

    def dump(self, n=0):
        m = list(self.member.dump(n=n))
        m[-1] = (m[-1][0], m[-1][1] + ';')
        return (e for e in m)


@node_type('a2ml_taggedstruct_type_name')
class TaggedStruct(TypeName):
    __slots__ = 'member',

    def __init__(self, identifier=None, member=None):
        self.member = list()
        super(TaggedStruct, self).__init__('taggedstruct', identifier, member)

    def __iter__(self):
        return (e for e in self.member)

    @property
    def required(self):
        return False

    def get_class(self, tokens, recurse=False):
        if self.tagged and not recurse:
            return super(TaggedStruct, self).get_class(tokens)
        else:
            kwargs = dict([(n.tag, list() if n.multiple else None) for n in self])
            while tokens:
                if tokens[0] in [n.tag for n in self]:
                    node = dict([(n.tag, n) for n in self])[tokens[0]]
                    if node.multiple:
                        kwargs[node.tag].append(node.get_class(tokens))
                    else:
                        kwargs[node.tag] = node.get_class(tokens)
                else:
                    break
            return AmlDynNode(list(), kwargs)

    def dump(self, n=0):
        return super(TaggedStruct, self).dump(n=n)


@node_type('a2ml_taggedstruct_member')
class TaggedStructMember(A2MLNode):
    __slots__ = 'type_name', 'multiple'

    def __init__(self, type_name, multiple):
        self.type_name = None
        self.multiple = multiple
        super(TaggedStructMember, self).__init__((type_name[0], type_name[1][1]))

    @property
    def tag(self):
        return self.type_name.tag

    def get_class(self, tokens):
        return self.type_name.get_class(tokens)

    def dump(self, n=0):
        t = list(self.type_name.dump(n=n))
        if not isinstance(self.type_name, BlockDefinition):
            t.insert(0, (n, '"{tag}"'.format(tag=self.tag)))
        if self.multiple:
            t[0] = (t[0][0], '(' + t[0][1])
            t[-1] = (t[-1][0], t[-1][1] + ')*;')
        else:
            t[-1] = (t[-1][0], t[-1][1] + ';')
        return (e for e in t)


@node_type('a2ml_taggedunion_type_name')
class TaggedUnion(TypeName):
    __slots__ = 'member',

    def __init__(self, identifier=None, member=None):
        self.member = list()
        super(TaggedUnion, self).__init__('taggedunion', identifier, member)

    def __iter__(self):
        return (e for e in self.member)

    @property
    def required(self):
        return False

    def get_class(self, tokens, recurse=False):
        if self.tagged and not recurse:
            return super(TaggedUnion, self).get_class(tokens)
        else:
            kwargs = dict()
            for node in self:
                if len(tokens) and tokens[0] == node.tag:
                    kwargs.setdefault(tokens[0], node.get_class(tokens))
                else:
                    kwargs.setdefault(node.tag, None)
            return AmlDynNode(list(), kwargs)

    def dump(self, n=0):
        return super(TaggedUnion, self).dump(n=n)


@node_type('a2ml_taggedunion_member')
class TaggedUnionMember(A2MLNode):
    __slots__ = 'tag', 'member'

    def __init__(self, tag, member):
        self.tag = None
        self.member = None
        super(TaggedUnionMember, self).__init__(tag, member)

    def get_class(self, tokens):
        tokens.pop(0)
        return self.member.get_class(tokens)

    def dump(self, n=0):
        t = list(self.member.dump(n=n))
        if not isinstance(self.member, BlockDefinition):
            t.insert(0, (n, '"{tag}"'.format(tag=self.tag)))
        t[-1] = (t[-1][0], t[-1][1] + ';')
        return (e for e in t)


@node_type('a2ml_enum_type_name')
class Enum(TypeName):
    __slots__ = 'enumerator',

    def __init__(self, identifier=None, enumerator=None):
        self.enumerator = list()
        super(Enum, self).__init__('enum', identifier, enumerator)

    def __iter__(self):
        return (e for e in self.enumerator)

    @property
    def required(self):
        return True

    def get_class(self, tokens, recurse=False):
        if self.tagged and not recurse:
            return super(Enum, self).get_class(tokens)
        else:
            return type('E', (str,), {})(tokens.pop(0))

    def dump(self, n=0):
        if self.is_def:
            yield n, '{node_type} {identifier}'.format(node_type=self.node_type, identifier=self.identifier)
        else:
            tmp = '{node_type}'
            if self.identifier:
                tmp += ' {identifier}'
            tmp += ' {{'
            yield n, tmp.format(node_type=self.node_type, identifier=self.identifier)
            for index, member in enumerate(self, start=1):
                for _n, e in member.dump(n=n + 1):
                    if index < len(self.enumerator):
                        yield (_n, e + ',')
                    else:
                        yield (_n, e)
            yield n, '}'


@node_type('a2ml_taggedstruct_definition')
class TaggedStructDefinition(A2MLNode):
    __slots__ = 'tag', 'member', 'multiple'

    def __init__(self, tag, member, multiple):
        self.tag = None
        self.member = None
        self.multiple = multiple
        super(TaggedStructDefinition, self).__init__(tag, member)

    def get_class(self, tokens):
        # the bellow code handles the case where the tagged struct definition's member is empty, for example:
        # taggedstruct {
        #     "SLAVE";
        #     "MASTER" struct {...};
        # };
        # where 'SLAVE' is the empty member.
        # this description seems to be used in a2ml examples available on the web, but doesn't seems to follow the
        # specification, as the latter defines the tagged struct definition as:
        # taggedstruct_definition ::= <tag> member | <tag> "("member")*"
        # where the member is not an optional element.
        # however, if the above case happens, the tag will be set to true, as it seems to be used as a flag.
        if len(tokens) and tokens[0] == self.tag:
            tokens.pop(0)
            if self.member is not None:
                return self.member.get_class(tokens)
            else:
                return True
        else:
            return None

    def dump(self, n=0):
        raise NotImplementedError


@node_type('a2ml_member')
class Member(A2MLNode):
    __slots__ = 'type_name', 'array_specifier'

    def __init__(self, type_name, array_specifier):
        self.type_name = None
        self.array_specifier = None
        super(Member, self).__init__(type_name, array_specifier)

    @property
    def required(self):
        return self.type_name.required

    @property
    def array_specifier_int(self):
        if self.array_specifier:
            tmp = 1
            for value in self.array_specifier:
                tmp *= value
            return tmp
        return 0

    def get_class(self, tokens):
        if self.array_specifier_int and not isinstance(self.type_name, (Char, UChar)):
            return AmlDynNode([self.type_name.get_class(tokens) for _ in range(self.array_specifier_int)], dict())
        else:
            return self.type_name.get_class(tokens)

    def dump(self, n=0):
        for e in self.type_name.dump(n=n):
            yield e
        if self.array_specifier:
            yield n, str(self.array_specifier)


@node_type('a2ml_enumerator')
class Enumerator(A2MLNode):
    __slots__ = 'keyword', 'constant'

    def __init__(self, keyword, constant=None):
        self.keyword = None
        self.constant = constant
        super(Enumerator, self).__init__(keyword)

    def get_class(self, tokens): return super(Enumerator, self).get_class(tokens)

    def dump(self, n=0):
        yield n, '"{k}"{e}{c}'.format(k=self.keyword,
                                      e=' = ' if self.constant is not None else '',
                                      c=self.constant)
