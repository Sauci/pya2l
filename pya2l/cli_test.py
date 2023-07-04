import json

import platform
import pytest
from collections import OrderedDict
from unittest.mock import Mock, patch, mock_open

from .cli import main

builtin_open = open


def get_call_args(m, index):
    _, minor, _ = platform.python_version_tuple()
    if int(minor) <= 7:
        return m.call_args_list[index][0]
    else:
        return m.call_args_list[index].args


def mapped_mock_open(file_contents_dict):
    mock_files = {}
    for file_name, content in file_contents_dict.items():
        mock_files[file_name] = mock_open(read_data=content).return_value
        mock_files[file_name].name = file_name

    def my_open(file_name, *args, **kwargs):
        if file_name in mock_files:
            return mock_files[file_name]
        else:
            return builtin_open(file_name, *args, **kwargs)

    mock_opener = Mock()
    mock_opener.side_effect = my_open
    return mock_opener


@pytest.mark.parametrize('indent_arg, indent', [
    # (('',), None), see https://github.com/golang/protobuf/issues/1121
    # (('-i', '0'), 0), see https://github.com/golang/protobuf/issues/1121
    (('-i', '1'), 1),
    (('-i', '2'), 2)])
@pytest.mark.parametrize('in_file_name', ['my_input.a2l'])
@pytest.mark.parametrize('out_file_name', ['my_output.json'])
@pytest.mark.parametrize('input_file_content, output_file_content', [
    ('ASAP2_VERSION 1 2 /begin PROJECT _ "" /end PROJECT'.encode(), OrderedDict({
        'ASAP2_VERSION': {
            'VersionNo': {'Value': 1, 'Base': 10, 'Size': 1},
            'UpgradeNo': {'Value': 2, 'Base': 10, 'Size': 1}
        },
        'PROJECT': {
            'Name': {
                'Value': "_"
            },
            'LongIdentifier': {}
        }
    }))])
def test_a2l_to_json_command(indent_arg,
                             indent,
                             in_file_name,
                             out_file_name,
                             input_file_content,
                             output_file_content):
    with patch("builtins.open", mock_open(read_data=input_file_content)) as m:
        m.return_value.name = in_file_name
        main(list(filter(lambda e: e != '', ['-v', in_file_name, 'to_json', '-o', out_file_name, *indent_arg])))
        assert get_call_args(m, 0) == (in_file_name, 'rb', -1, None, None)
        assert get_call_args(m, 1) == (out_file_name, 'wb', -1, None, None)
        assert get_call_args(m.return_value.write, 0) == (json.dumps(output_file_content, indent=indent).encode(),)


@pytest.mark.parametrize('indent_arg, indent', [
    # (('',), None), see https://github.com/golang/protobuf/issues/1121
    # (('-i', '0'), 0), see https://github.com/golang/protobuf/issues/1121
    (('-i', '1'), 1),
    (('-i', '2'), 2)])
@pytest.mark.parametrize('in_file_name', ['my_input.json'])
@pytest.mark.parametrize('out_file_name', ['my_output.json'])
@pytest.mark.parametrize('input_file_content, output_file_content', [
    (json.dumps(OrderedDict({
        'ASAP2_VERSION': {
            'VersionNo': {'Value': 1, 'Base': 10, 'Size': 1},
            'UpgradeNo': {'Value': 2, 'Base': 10, 'Size': 1}
        },
        'PROJECT': {
            'Name': {
                'Value': "_"
            },
            'LongIdentifier': {}
        }
    })).encode(), OrderedDict({
        'ASAP2_VERSION': {
            'VersionNo': {'Value': 1, 'Base': 10, 'Size': 1},
            'UpgradeNo': {'Value': 2, 'Base': 10, 'Size': 1}
        },
        'PROJECT': {
            'Name': {
                'Value': "_"
            },
            'LongIdentifier': {}
        }
    }))])
def test_json_to_json_command(indent_arg,
                              indent,
                              in_file_name,
                              out_file_name,
                              input_file_content,
                              output_file_content):
    with patch("builtins.open", mock_open(read_data=input_file_content)) as mock_file:
        mock_file.return_value.name = in_file_name
        main(list(filter(lambda e: e != '', ['-v', in_file_name, 'to_json', '-o', out_file_name, *indent_arg])))
        assert get_call_args(mock_file, 0) == (in_file_name, 'rb', -1, None, None)
        assert get_call_args(mock_file, 1) == (out_file_name, 'wb', -1, None, None)
        assert get_call_args(mock_file.return_value.write, 0) == \
               (json.dumps(output_file_content, indent=indent).encode(),)


@pytest.mark.parametrize('left_input_file_name', ['my_left_input.json'])
@pytest.mark.parametrize('right_input_file_name', ['my_right_input.json'])
@pytest.mark.parametrize('left_input_file_content, right_input_file_content, output_content', [
    (json.dumps({
        'ASAP2_VERSION': {
            'UpgradeNo': {'Base': 10, 'Size': 1, 'Value': 2},
            'VersionNo': {'Base': 10, 'Size': 1, 'Value': 1}
        }
    }).encode(), json.dumps({
        'ASAP2_VERSION': {
            'UpgradeNo': {'Base': 10, 'Size': 1, 'Value': 2},
            'VersionNo': {'Base': 10, 'Size': 1, 'Value': 1}
        }
    }).encode(),
     ''),
    (json.dumps({
        'ASAP2_VERSION': {
            'UpgradeNo': {'Base': 10, 'Size': 1, 'Value': 2},
            'VersionNo': {'Base': 10, 'Size': 1, 'Value': 1}
        }
    }).encode(), json.dumps({
        'ASAP2_VERSION': {
            'UpgradeNo': {'Base': 16, 'Size': 1, 'Value': 2},
            'VersionNo': {'Base': 10, 'Size': 1, 'Value': 1}
        }
    }).encode(),
     '(\'change\', \'ASAP2_VERSION.UpgradeNo.Base\', (10, 16))')
])
def test_diff_command(capsys,
                      left_input_file_name,
                      right_input_file_name,
                      left_input_file_content,
                      right_input_file_content,
                      output_content):
    with patch("builtins.open", mapped_mock_open({left_input_file_name: left_input_file_content,
                                                  right_input_file_name: right_input_file_content})) as m:
        main(list(filter(lambda e: e != '', [left_input_file_name, 'diff', right_input_file_name])))
        assert get_call_args(m, 0) == (left_input_file_name, 'rb', -1, None, None)
        assert get_call_args(m, 1) == (right_input_file_name, 'rb', -1, None, None)
        assert capsys.readouterr().out == output_content
