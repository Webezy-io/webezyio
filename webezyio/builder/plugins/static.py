# Copyright (c) 2022 Webezy.io.

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

gitignore_py = '# Byte-compiled / optimized / DLL files\n\
__pycache__/\n\
*.py[cod]\n\
*$py.class\n\n\
# C extensions\n\
*.so\n\n\
# Distribution / packaging\n\
.Python\n\
build/\n\
develop-eggs/\n\
dist/\n\
downloads/\n\
eggs/\n\
.eggs/\n\
lib/\n\
lib64/\n\
parts/\n\
sdist/\n\
var/\n\
wheels/\n\
share/python-wheels/\n\
*.egg-info/\n\
.installed.cfg\n\
*.egg\n\
MANIFEST\n\n\
# PyInstaller\n\
#  Usually these files are written by a python script from a template\n\
#  before PyInstaller builds the exe, so as to inject date/other infos into it.\n\
*.manifest\n\
*.spec\n\n\
# Installer logs\n\
pip-log.txt\n\
pip-delete-this-directory.txt\n\
# Unit test / coverage reports\n\
htmlcov/\n\
.tox/\n\
.nox/\n\
.coverage\n\
.coverage.*\n\
.cache\n\
nosetests.xml\n\
coverage.xml\n\
*.cover\n\
*.py,cover\n\
.hypothesis/\n\
.pytest_cache/\n\
cover/\n\n\
# Translations\n\
*.mo\n\
*.pot\n\
# Webezy stuff:\n\
.webezy/\n\
# Flask stuff:\n\
instance/\n\
.webassets-cache\n\
# Scrapy stuff:\n\
.scrapy\n\
# Sphinx documentation\n\
docs/_build/\n\
# PyBuilder\n\
.pybuilder/\n\
target/\n\
# Jupyter Notebook\n\
.ipynb_checkpoints\n\
# IPython\n\
profile_default/\n\
ipython_config.py\n\n\
# Environments\n\n\
.env\n\
.venv\n\
env/\n\
venv/\n\
ENV/\n\
env.bak/\n\
venv.bak/\n'

gitignore_go = '# If you prefer the allow list template instead of the deny list, see community template:\n\
# https://github.com/github/gitignore/blob/main/community/Golang/Go.AllowList.gitignore\n\
#\n\
# Binaries for programs and plugins\n\
*.exe\n\
*.exe~\n\
*.dll\n\
*.so\n\
*.dylib\n\n\
# Test binary, built with `go test -c`\n\
*.test\n\n\
# Output of the go coverage tool, specifically when used with LiteIDE\n\
*.out\n\n\
# Dependency directories (remove the comment below to include it)\n\n\
# vendor/\n\n\
# Go workspace file\n\
go.work'

gitignore_ts = 'lib-cov\n\
*.seed\n\
*.log\n\
*.csv\n\
*.dat\n\
*.out\n\
*.pid\n\
*.gz\n\
*.swp\n\n\
pids\n\
logs\n\
results\n\
tmp\n\n\
# Build\n\
public/css/main.css\n\n\
# Coverage reports\n\n\
coverage\n\n\
# API keys and secrets\n\
.env\n\n\
# Dependency directory\n\
node_modules\n\
bower_components\n\n\
# Editors\n\
.idea\n\
*.iml\n\
# OS metadata\n\
.DS_Store\n\
Thumbs.db\n\n\
# Ignore built ts files\n\
dist/**/*\n\
# ignore yarn.lock\n\
yarn.lock\n\n\
.webezy\n'
_OPEN_BRCK='{'
_CLOSING_BRCK = '}'

def bash_init_script_go(project_package, services, packages):
    services_protoc = []
    packages_protoc = []
    for s in services:
        services_protoc.append('protoc -I=$SRC_DIR --go_out=$DST_DIR --go_opt=paths=source_relative --go-grpc_out=$DST_DIR"/{0}"  --go-grpc_opt=paths=source_relative protos/{0}.proto'.format(s))
    for p in packages:
        packages_protoc.append('protoc -I=$SRC_DIR --go_out=$DST_DIR --go_opt=paths=source_relative --go-grpc_out=$DST_DIR"/{0}"  --go-grpc_opt=paths=source_relative protos/{0}.proto'.format(p))
    return '#!/bin/bash\n\n\
echo "[WEBEZYIO] init.sh starting protoc compiler for Go"\n\
go get -u google.golang.org/protobuf\n\
go get -u google.golang.org/grpc\n\
SRC_DIR="protos"\n\
DST_DIR="services/protos"\n\
{1}\n\
{2}\n\
go mod tidy\n\
go test\n\
statuscode=$?\n\
echo "Exit code for go.mod tidy and test -> "$statuscode\n\
[[ "$statuscode" != "0" ]] && {3} echo "Some error occured during init script for Go"; echo "Running init for : github.com/{0}"; go mod init github.com/{0}; {4}\n'.format(project_package,'\n'.join(services_protoc),'\n'.join(packages_protoc),_OPEN_BRCK,_CLOSING_BRCK)

bash_init_script_ts = '#!/bin/bash\n\n\
echo "[WEBEZYIO] init.sh starting protoc compiler"\n\
npm i\n\
node ./bin/proto.js\n\
npm run build\n\
statuscode=$?\n\
echo "Exit code for protoc -> "$statuscode\n\
[[ "$statuscode" != "0" ]] && { echo "Some error occured during init script"; exit 1; }\n\
exit 0'

bash_init_script_webpack = '#!/bin/bash\n\
declare -a services=("protos")\n\
for SERVICE in "${0}services[@]{1}"; do\n\
    echo $SERVICE\n\
    cd $SERVICE\n\
    for FILE in *; do\n\
        filename=$FILE\n\
        search="protos\/"\n\
        replace=""\n\
        sed -i\'.bak\' -e "1,8 s/$search/$replace/gi" $filename\n\
        rm -f *.bak\n\
        echo "[webezy-script] Compiling -> "$filename\n\
        sudo protoc -I=../protos $filename  --js_out=import_style=commonjs,binary:../clients/webpack   --grpc-web_out=import_style=typescript,mode=grpcwebtext:../clients/webpack\n\
    done\n\
done'.format(_OPEN_BRCK,_CLOSING_BRCK)

bash_run_server_script_ts = '#!/bin/bash\n\n\
if [[ $1 == "debug" ]]\n\
then\n\
\techo "Debug mode: $1"\n\
\tGRPC_VERBOSITY=DEBUG GRPC_TRACE=all node ./server/server.js\n\
else\n\
\tnode ./server/server.js\n\
fi'

protos_compile_script_ts = 'const path = require("path");\n\
const { execSync } = require("child_process");\n\
const rimraf = require("rimraf");\n\n\
const PROTO_DIR = path.join(__dirname, "../protos");\n\
const MODEL_DIR = path.join(__dirname, "../services/protos");\n\
const PROTOC_PATH = path.join(__dirname, "../node_modules/grpc-tools/bin/protoc");\n\
const PLUGIN_PATH = path.join(__dirname, "../node_modules/.bin/protoc-gen-ts_proto");\n\n\
rimraf.sync(`${MODEL_DIR}/*.ts`, {\n\
  glob: { ignore: `${MODEL_DIR}/tsconfig.json` },\n\
});\n\n\
const protoConfig = [\n\
  `--plugin=${PLUGIN_PATH}`,\n\n\
  // https://github.com/stephenh/ts-proto/blob/main/README.markdown\n\
  "--ts_proto_opt=outputServices=grpc-js,env=node,useOptionals=messages,exportCommonSymbols=false,esModuleInterop=true",\n\n\
  `--ts_proto_out=${MODEL_DIR}`,\n\
  `--proto_path ${PROTO_DIR} ${PROTO_DIR}/*.proto`,\n\
];\n\n\
// https://github.com/stephenh/ts-proto#usage\n\
execSync(`${PROTOC_PATH} ${protoConfig.join(" ")}`);\n\
console.log(`> Proto models created: ${MODEL_DIR}`);'

package_json ='{\n\
    "name": "REPLACEME",\n\
    "version": "1.0.0",\n\
    "description": "This project has been generated thanks to ```Webezy.io``` CLI. For start using it please run  ```sh webezy run --build```  and see the magic in action. For more information please visit https://www.webezy.io/docs",\n\
    "main": "bin/proto.js",\n\
    "scripts": {\n\
        "test": "echo \\"Error: no test specified\\" && exit 1",\n\
        "lint": "eslint --ext .ts .",\n\
        "build": "node bin/proto && rimraf clients/typescript/protos && rimraf server && tsc -b",\n\
        "build:webpack": "bash bin/webpack.sh",\n\
        "start": "node clients/typescript/server",\n\
        "client": "node clients/typescript/client",\n\
        "health": "node clients/typescript/health"\n\
    },\n\
    "author": "",\n\
    "license": "ISC",\n\
    "dependencies": {\n\
        "@grpc/grpc-js": "^1.6.12",\n\
        "rxjs": "^7.5.6"\n\
    },\n\
    "devDependencies": {\n\
        "@types/node": "^18.7.14",\n\
        "@typescript-eslint/eslint-plugin": "^5.36.1",\n\
        "@typescript-eslint/parser": "^5.36.1",\n\
        "eslint": "^8.23.0",\n\
        "eslint-config-airbnb-base": "^15.0.0",\n\
        "eslint-config-airbnb-typescript": "^17.0.0",\n\
        "eslint-plugin-import": "^2.26.0",\n\
        "eslint-plugin-sonarjs": "^0.15.0",\n\
        "grpc-tools": "^1.11.2",\n\
        "rimraf": "^3.0.2",\n\
        "ts-proto": "^1.123.1",\n\
        "typescript": "^4.8.2",\n\
        "ts-node": "^10.9.1"\n\
    }\n\
}'

package_json_webpack = '{\n\
  "name": "REPLACEME",\n\
  "version": "1.0.0",\n\
  "description": "This project has been generated thanks to ```Webezy.io``` CLI. For start using it please run  ```webezy build && wz run```  and see the magic in action. For more information please visit https://www.webezy.io/docs",\n\
  "scripts": {\n\
    "build": "echo \\"Error: no build specified\\" && exit 1",\n\
    "test": "echo \\"Error: no test specified\\" && exit 1",\n\
    "dev": "echo \\"Error: no dev specified\\" && exit 1",\n\
    "start": "echo \\"Error: no start specified\\" && exit 1"\n\
  },\n\
  "author": "",\n\
  "license": "Apache-2.0",\n\
  "devDependencies": {\n\
    "@types/google-protobuf": "^3.15.6"\n\
  },\n\
  "engines": {\n\
    "node": ">=14"\n\
  },\n\
  "dependencies": {\n\
    "@grpc/grpc-js": "~1.1.8",\n\
    "@grpc/proto-loader": "~0.5.4",\n\
    "async": "~3.2.3",\n\
    "google-protobuf": "~3.14.0",\n\
    "grpc-web": "~1.4.2",\n\
    "lodash": "~4.17.0",\n\
    "webpack": "~4.43.0",\n\
    "webpack-cli": "~3.3.11"\n\
  }\n\
}'

utils_errors_ts = 'import { Metadata, ServiceError as grpcServiceError, status } from \'@grpc/grpc-js\';\n\n\
/**\n\
 * https://grpc.io/grpc/node/grpc.html#~ServiceError__anchor\n\
 */\n\
export class ServiceError extends Error implements Partial<grpcServiceError> {\n\
	public override name: string = \'ServiceError\';\n\n\
	constructor(\n\
		public code: status,\n\
		public override message: string,\n\
		public details?: string,\n\
		public metadata?: Metadata,\n\
	) {\n\
		super(message);\n\
	}\n\
}'

utils_interfaces = '// Insert here more interfaces to service will be able to speak with\n\
interface Api<T> {\n\
	[method: string]: T;\n\
}\n\n\
export type ApiType<T> = Api<T> & {\n\
\n\
}'

main_ts_config = '{\n\
    "compilerOptions": {\n\
        "baseUrl": ".",\n\
        "paths": {},\n\
        "target": "ES2019",\n\
        "outDir": "server",\n\
        "module": "commonjs",\n\
        "moduleResolution": "node",\n\
        "incremental": true,\n\
        "declaration": true,\n\
        "newLine": "lf",\n\
        "strict": true,\n\
        "allowUnreachableCode": false,\n\
        "allowUnusedLabels": false,\n\
        "noFallthroughCasesInSwitch": true,\n\
        "noImplicitOverride": true,\n\
        "noImplicitReturns": true,\n\
        "noPropertyAccessFromIndexSignature": true,\n\
        "noUnusedLocals": false,\n\
        "noUnusedParameters": false,\n\
        "removeComments": false,\n\
        "sourceMap": true,\n\
        "forceConsistentCasingInFileNames": true,\n\
        "esModuleInterop": true,\n\
        "skipLibCheck": true\n\
    },\n\
    "include": [\n\
        "services/**/*",\n\
        "services/*.ts",\n\
        "*.ts"\n\
    ],\n\
    "exclude": [\n\
        "node_modules",\n\
        "services/protos"\n\
    ],\n\
    "references": [\n\
        {\n\
            "path": "services/protos"\n\
        }\n\
    ]\n\
}'

clients_ts_configs = '{\n\
    "extends": "../tsconfig.json",\n\
    "compilerOptions": {\n\
        "composite": true,\n\
        "outDir": "../clients/typescript",\n\
        "noImplicitReturns": false\n\
    },\n\
    "include": [\n\
        "client.ts","protos/**/*","protos/*.ts"\n\
    ],\n\
    "exclude": [\n\
        "node_modules"\n\
    ]\n\
}'

protos_ts_config = '{\n\
    "extends": "../../tsconfig.json",\n\
    "compilerOptions": {\n\
        "composite": true,\n\
        "outDir": "../../server/services/protos",\n\
        "noImplicitReturns": false\n\
    },\n\
    "include": [\n\
        "*","google/**/*"\n\
    ],\n\
    "exclude": [\n\
        "node_modules"\n\
    ]\n\
}'


main_ts_config_client_only = '{\n\
    "compilerOptions": {\n\
        "baseUrl": ".",\n\
        "paths": {},\n\
        "target": "ES2019",\n\
        "outDir": "clients/typescript",\n\
        "module": "commonjs",\n\
        "moduleResolution": "node",\n\
        "incremental": true,\n\
        "declaration": true,\n\
        "newLine": "lf",\n\
        "strict": true,\n\
        "allowUnreachableCode": false,\n\
        "allowUnusedLabels": false,\n\
        "noFallthroughCasesInSwitch": true,\n\
        "noImplicitOverride": true,\n\
        "noImplicitReturns": true,\n\
        "noPropertyAccessFromIndexSignature": true,\n\
        "noUnusedLocals": false,\n\
        "noUnusedParameters": false,\n\
        "removeComments": false,\n\
        "sourceMap": true,\n\
        "forceConsistentCasingInFileNames": true,\n\
        "esModuleInterop": true,\n\
        "skipLibCheck": true\n\
    },\n\
    "include": [\n\
        "services/**/*",\n\
        "services/*.ts",\n\
    ],\n\
    "exclude": [\n\
        "node_modules",\n\
        "services/protos"\n\
    ],\n\
    "references": [\n\
        {\n\
            "path": "services/protos"\n\
        }\n\
    ]\n\
}'

protos_ts_config_client_only = '{\n\
    "extends": "../../tsconfig.json",\n\
    "compilerOptions": {\n\
        "composite": true,\n\
        "outDir": "../../clients/typescript/protos",\n\
        "noImplicitReturns": false\n\
    },\n\
    "include": [\n\
        "*","google/**/*"\n\
    ],\n\
    "exclude": [\n\
        "node_modules"\n\
    ]\n\
}'

bash_run_server_script_go = '#!/bin/bash\n\n\
if [[ $1 == "debug" ]]\n\
then\n\
\techo "Debug mode: $1"\n\
\tGRPC_VERBOSITY=DEBUG GRPC_TRACE=all ngo run ./server/server.go\n\
else\n\
go run ./server/server.go\n\
fi'

utils_go = 'package utils\n\n\
import (\n\
	"log"\n\
)\n\n\
var (\n\
	WarningLogger *log.Logger\n\
	DebugLogger   *log.Logger\n\
	InfoLogger    *log.Logger\n\
	ErrorLogger   *log.Logger\n\
)\n\n\
func init() {\n\
	InfoLogger = log.New(log.Writer(), "INFO: ", log.Ldate|log.Ltime|log.Lshortfile)\n\
	DebugLogger = log.New(log.Writer(), "DEBUG: ", log.Ldate|log.Ltime|log.Lshortfile)\n\
	WarningLogger = log.New(log.Writer(), "WARNING: ", log.Ldate|log.Ltime|log.Lshortfile)\n\
	ErrorLogger = log.New(log.Writer(), "ERROR: ", log.Ldate|log.Ltime|log.Lshortfile)\n\
}'