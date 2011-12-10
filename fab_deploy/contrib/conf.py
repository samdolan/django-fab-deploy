from fabric.api import env
import os
import yaml

try:
    # python 2.7+
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

# Originally from https://gist.github.com/844388
class OrderedDictYAMLLoader(yaml.Loader):
    """
    A YAML loader that loads mappings into ordered dictionaries.
    """

    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)

        self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(None, None,
                'expected a mapping node, but found %s' % node.id, node.start_mark)

        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError, exc:
                raise yaml.constructor.ConstructorError('while constructing a mapping',
                    node.start_mark, 'found unacceptable key (%s)' % exc, key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping


def set_yaml_config(configuration_path, env_overrides={}):
    """Update the environment dictionary with the yaml file at the
    given path."""
    with open(configuration_path) as config_file:
        config = yaml.load(config_file, OrderedDictYAMLLoader)

    config.update(env_overrides)

    # TODO: Make replacement recursive
    for k, v in config.iteritems():
        if isinstance(v, basestring):
            env[k] = os.path.expanduser(v) % env
        else:
            env[k] = v


    import pprint
    from fabric.colors import green
    print green('*' * 80)
    print green("Environment Dictionary: \n%s" % pprint.pprint(env))
    print green('*' * 80)

