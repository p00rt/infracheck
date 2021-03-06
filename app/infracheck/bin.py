
# pragma: no cover

import sys
import os
import argparse
import json

t = sys.argv[0].replace(os.path.basename(sys.argv[0]), "") + "/../"

if os.path.isdir(t):
    sys.path.append(t)

from .controller import Controller

#
# Arguments parsing
#
parser = argparse.ArgumentParser()
parser.add_argument(
    '--list-available-types',
    help='List all available check types that can be used',
    default=False,
    action='store_true'
)
parser.add_argument(
    '--list-all-configurations',
    help='List all configured checks',
    default=False,
    action='store_true'
)
parser.add_argument(
    '--list-enabled-configurations',
    help='List only enabled configurations',
    default=False,
    action='store_true'
)
parser.add_argument(
    '--directory',
    help='Alternative project directory',
    default=''
)
parser.add_argument(
    '--server',
    help='Spawn a HTTP server at 7422 port',
    default=False,
    action='store_true'
)
parser.add_argument(
    '--server-port',
    help='Server port, default is 7422',
    default=7422
)
parser.add_argument(
    '--server-path-prefix',
    help='Optional path prefix to the routing, eg. /this-is-a-secret will make urls looking like: '
         'http://localhost:8000/this-is-a-secret/',
    default=''
)

parsed = parser.parse_args()
project_dir = parsed.directory if parsed.directory else os.getcwd()
server_port = int(parsed.server_port if parsed.server_port else 7422)
server_path_prefix = parsed.server_path_prefix if parsed.server_path_prefix else ''

app = Controller(project_dir, server_port, server_path_prefix)

if parsed.server:
    app.spawn_server()
    sys.exit(0)

# action: --list-all-configurations
if parsed.list_all_configurations:
    for name in app.list_enabled_configs():
        print(name)

    sys.exit(0)

# action: --list-available-types
if parsed.list_available_types:
    for name in app.list_available_checks():
        print(name)

    sys.exit(0)

# action: --list-enabled-configurations
if parsed.list_enabled_configurations:
    for name in app.list_all_configs():
        print(name)

    sys.exit(0)

# action: perform health checking
result = app.perform_checks()
print(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))

if not result['global_status']:
    sys.exit(1)

sys.exit(0)
