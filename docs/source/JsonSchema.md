# Webezy.io Json Schema

You can add this schema to enable intelisense on VSCode:
Open the vs-code settings (Json) - mac (cmd+shift+p) | win (ctrl+shift+p) and enter `Open settings (Json)`

Thie will add a support for auto-completion and json schema validation inside vscode for your `webezy.json` files accross all your projects

```json
{
    "json.schemas": [
        {
            "fileMatch": [
                "/webezy.json"
            ],
            "schema": {
                "description": "[webezy.WebezyJson.v1.WebezyJson] - The webezy.json file schema",
                "type": "object",
                "properties": {
                    "domain": {
                        "description": "[webezy.WebezyJson.v1.WebezyJson.domain] - The domain name without any prefix or suffix",
                        "type": "string"
                    },
                    "project": {
                        "description": "[webezy.WebezyJson.v1.WebezyJson.project] - The webezy project description",
                        "$ref": "#/definitions/WebezyProject"
                    },
                    "config": {
                        "description": "[webezy.WebezyJson.v1.WebezyJson.config] - The webezy project configs",
                        "$ref": "#/definitions/WebezyConfig"
                    },
                    "services": {
                        "description": "[webezy.WebezyJson.v1.WebezyJson.services] -",
                        "type": "object",
                        "additionalProperties": {
                            "$ref": "#/definitions/WebezyService"
                        },
                        "propertyOrder": []
                    },
                    "packages": {
                        "description": "[webezy.WebezyJson.v1.WebezyJson.packages] -",
                        "type": "object",
                        "additionalProperties": {
                            "$ref": "#/definitions/WebezyPackage"
                        },
                        "propertyOrder": []
                    }
                },
                "propertyOrder": [
                    "domain",
                    "project",
                    "config",
                    "services",
                    "packages"
                ],
                "required": [
                    "domain",
                    "packages",
                    "services"
                ],
                "definitions": {
                    "WebezyProject": {
                        "description": "[webezy.WebezyCore.v1.WebezyProject] - The webezy project description",
                        "type": "object",
                        "properties": {
                            "uri": {
                                "description": "[webezy.WebezyCore.v1.WebezyProject.uri] - The project URI of root directory where the webezy.json file exists",
                                "type": "string"
                            },
                            "name": {
                                "description": "[webezy.WebezyCore.v1.WebezyProject.name] - Project full display name",
                                "type": "string"
                            },
                            "packageName": {
                                "description": "[webezy.WebezyCore.v1.WebezyProject.package_name] - project name code compatiable",
                                "type": "string"
                            },
                            "version": {
                                "description": "[webezy.WebezyCore.v1.WebezyProject.version] - The project version following SEMVER semantics",
                                "type": "string"
                            },
                            "type": {
                                "description": "[webezy.WebezyCore.v1.WebezyProject.type] - The project resource type",
                                "type": "string"
                            },
                            "kind": {
                                "description": "[webezy.WebezyCore.v1.WebezyProject.kind] - The project resource kind",
                                "type": "string"
                            },
                            "properties": {
                                "description": "[webezy.WebezyCore.v1.WebezyProject.properties] - Additional project properties",
                                "type": "object",
                                "additionalProperties": {},
                                "propertyOrder": []
                            },
                            "server": {
                                "description": "[webezy.WebezyCore.v1.WebezyProject.server] - The project attached server descriptin",
                                "$ref": "#/definitions/WebezyServer"
                            },
                            "clients": {
                                "description": "[webezy.WebezyCore.v1.WebezyProject.clients] - The project assigned clients array",
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/WebezyClient"
                                }
                            },
                            "goPackage": {
                                "description": "[webezy.WebezyCore.v1.WebezyProject.go_package] - The go compatiable package name",
                                "type": "string"
                            }
                        },
                        "propertyOrder": [
                            "uri",
                            "name",
                            "packageName",
                            "version",
                            "type",
                            "kind",
                            "properties",
                            "server",
                            "clients",
                            "goPackage"
                        ],
                        "required": [
                            "clients",
                            "kind",
                            "name",
                            "packageName",
                            "type",
                            "uri",
                            "version"
                        ]
                    },
                    "WebezyServer": {
                        "description": "[webezy.WebezyCore.v1.WebezyServer] - The description for webezy server",
                        "type": "object",
                        "properties": {
                            "language": {
                                "$ref": "#/definitions/WebezyLanguage",
                                "description": "[webezy.WebezyCore.v1.WebezyServer.language] - The server language"
                            }
                        },
                        "propertyOrder": [
                            "language"
                        ],
                        "required": [
                            "language"
                        ]
                    },
                    "WebezyLanguage": {
                        "description": "[webezy.WebezyCore.v1.WebezyLanguage] - None",
                        "enum": [
                            -1,
                            "UNKNONW_WEBEZYLANGUAGE",
                            "python",
                            "typescript",
                            "go"
                        ],
                        "type": "string"
                    },
                    "WebezyClient": {
                        "description": "[webezy.WebezyCore.v1.WebezyClient] - The description for webezy client",
                        "type": "object",
                        "properties": {
                            "language": {
                                "$ref": "#/definitions/WebezyLanguage",
                                "description": "[webezy.WebezyCore.v1.WebezyClient.language] - The client language"
                            },
                            "outDir": {
                                "description": "[webezy.WebezyCore.v1.WebezyClient.out_dir] - The output path for the client code modules",
                                "type": "string"
                            }
                        },
                        "propertyOrder": [
                            "language",
                            "outDir"
                        ],
                        "required": [
                            "language",
                            "outDir"
                        ]
                    },
                    "WebezyConfig": {
                        "description": "[webezy.WebezyConfig.v1.WebezyConfig] - The main configuration structure",
                        "type": "object",
                        "properties": {
                            "host": {
                                "description": "[webezy.WebezyConfig.v1.WebezyConfig.host] - The webezy.io server host",
                                "type": "string"
                            },
                            "port": {
                                "description": "[webezy.WebezyConfig.v1.WebezyConfig.port] - The server port",
                                "type": "number"
                            },
                            "deployment": {
                                "$ref": "#/definitions/DeploymentType",
                                "description": "[webezy.WebezyConfig.v1.WebezyConfig.deployment] - The project deployment type"
                            },
                            "proxy": {
                                "description": "[webezy.WebezyConfig.v1.WebezyConfig.proxy] -",
                                "$ref": "#/definitions/ProxyConfig"
                            },
                            "docs": {
                                "description": "[webezy.WebezyConfig.v1.WebezyConfig.docs] -",
                                "$ref": "#/definitions/WebezyDocs"
                            },
                            "template": {
                                "description": "[webezy.WebezyConfig.v1.WebezyConfig.template] -",
                                "$ref": "#/definitions/TemplateConfig"
                            },
                            "monitor": {
                                "description": "[webezy.WebezyConfig.v1.WebezyConfig.monitor] -",
                                "$ref": "#/definitions/WebezyMonitor"
                            },
                            "analytics": {
                                "description": "[webezy.WebezyConfig.v1.WebezyConfig.analytics] -",
                                "type": "boolean"
                            },
                            "token": {
                                "description": "[webezy.WebezyConfig.v1.WebezyConfig.token] -",
                                "type": "string"
                            },
                            "firstRun": {
                                "description": "[webezy.WebezyConfig.v1.WebezyConfig.first_run] -",
                                "type": "boolean"
                            },
                            "webezyioTemplates": {
                                "description": "[webezy.WebezyConfig.v1.WebezyConfig.webezyio_templates] -",
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "features": {
                                "description": "[webezy.WebezyConfig.v1.WebezyConfig.features] -",
                                "type": "object",
                                "additionalProperties": {
                                    "type": "boolean"
                                },
                                "propertyOrder": []
                            },
                            "plugins": {
                                "description": "[webezy.WebezyConfig.v1.WebezyConfig.plugins] -",
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            }
                        },
                        "propertyOrder": [
                            "host",
                            "port",
                            "deployment",
                            "proxy",
                            "docs",
                            "template",
                            "monitor",
                            "analytics",
                            "token",
                            "firstRun",
                            "webezyioTemplates",
                            "features",
                            "plugins"
                        ],
                        "required": [
                            "deployment",
                            "host",
                            "port"
                        ]
                    },
                    "DeploymentType": {
                        "description": "[webezy.WebezyConfig.v1.DeploymentType] - None",
                        "enum": [
                            "UNKNOWN_DEPLOYMENTTYPE",
                            "LOCAL",
                            "DOCKER"
                        ],
                        "type": "string"
                    },
                    "ProxyConfig": {
                        "description": "[webezy.WebezyProxy.v1.ProxyConfig] - The main configurations for envoy proxy",
                        "type": "object",
                        "properties": {
                            "admin": {
                                "description": "[webezy.WebezyProxy.v1.ProxyConfig.admin] - The admin configurations",
                                "$ref": "#/definitions/ProxyAddress"
                            },
                            "stats": {
                                "description": "[webezy.WebezyProxy.v1.ProxyConfig.stats] - The proxy stats sink configurations",
                                "$ref": "#/definitions/ProxyStatsSink"
                            },
                            "listeners": {
                                "description": "[webezy.WebezyProxy.v1.ProxyConfig.listeners] - The proxy listeners",
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/ProxyListener"
                                }
                            },
                            "clusters": {
                                "description": "[webezy.WebezyProxy.v1.ProxyConfig.clusters] - The proxy clusters",
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/ProxyCluster"
                                }
                            }
                        },
                        "propertyOrder": [
                            "admin",
                            "stats",
                            "listeners",
                            "clusters"
                        ],
                        "required": [
                            "clusters",
                            "listeners"
                        ]
                    },
                    "ProxyAddress": {
                        "description": "[webezy.WebezyProxy.v1.ProxyAddress] - The proxy settings global address",
                        "type": "object",
                        "properties": {
                            "address": {
                                "description": "[webezy.WebezyProxy.v1.ProxyAddress.address] - The address for the proxy",
                                "type": "string"
                            },
                            "port": {
                                "description": "[webezy.WebezyProxy.v1.ProxyAddress.port] - The proxy address port",
                                "type": "number"
                            }
                        },
                        "propertyOrder": [
                            "address",
                            "port"
                        ],
                        "required": [
                            "address",
                            "port"
                        ]
                    },
                    "ProxyStatsSink": {
                        "description": "[webezy.WebezyProxy.v1.ProxyStatsSink] - The proxy stats sink",
                        "type": "object",
                        "properties": {
                            "tcpClusterName": {
                                "description": "[webezy.WebezyProxy.v1.ProxyStatsSink.tcp_cluster_name] - The same cluster name as specified at the clusters array",
                                "type": "string"
                            },
                            "prefix": {
                                "description": "[webezy.WebezyProxy.v1.ProxyStatsSink.prefix] -",
                                "type": "string"
                            }
                        },
                        "propertyOrder": [
                            "tcpClusterName",
                            "prefix"
                        ],
                        "required": [
                            "prefix",
                            "tcpClusterName"
                        ]
                    },
                    "ProxyListener": {
                        "description": "[webezy.WebezyProxy.v1.ProxyListener] - The proxy listener configs",
                        "type": "object",
                        "properties": {
                            "name": {
                                "description": "[webezy.WebezyProxy.v1.ProxyListener.name] - The listsener name",
                                "type": "string"
                            },
                            "address": {
                                "description": "[webezy.WebezyProxy.v1.ProxyListener.address] - The listener address details",
                                "$ref": "#/definitions/ProxyAddress"
                            }
                        },
                        "propertyOrder": [
                            "name",
                            "address"
                        ],
                        "required": [
                            "name"
                        ]
                    },
                    "ProxyCluster": {
                        "description": "[webezy.WebezyProxy.v1.ProxyCluster] - The proxy cluster details",
                        "type": "object",
                        "properties": {
                            "name": {
                                "description": "[webezy.WebezyProxy.v1.ProxyCluster.name] - The cluster name",
                                "type": "string"
                            },
                            "endpoints": {
                                "description": "[webezy.WebezyProxy.v1.ProxyCluster.endpoints] - The cluster endpoints",
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/ProxyEndpoint"
                                }
                            }
                        },
                        "propertyOrder": [
                            "name",
                            "endpoints"
                        ],
                        "required": [
                            "endpoints",
                            "name"
                        ]
                    },
                    "ProxyEndpoint": {
                        "description": "[webezy.WebezyProxy.v1.ProxyEndpoint] - The proxy endpoint config",
                        "type": "object",
                        "properties": {
                            "address": {
                                "description": "[webezy.WebezyProxy.v1.ProxyEndpoint.address] - The endpoint address",
                                "$ref": "#/definitions/ProxyAddress"
                            }
                        },
                        "propertyOrder": [
                            "address"
                        ]
                    },
                    "WebezyDocs": {
                        "description": "[webezy.WebezyConfig.v1.WebezyDocs] - Main configurations for Auto generated docs",
                        "type": "object",
                        "properties": {
                            "file": {
                                "description": "[webezy.WebezyConfig.v1.WebezyDocs.file] - The main README.md file path should be placed with different path if you want to write custom README.md file",
                                "type": "string"
                            }
                        },
                        "propertyOrder": [
                            "file"
                        ],
                        "required": [
                            "file"
                        ]
                    },
                    "TemplateConfig": {
                        "description": "[webezy.WebezyTemplate.v1.TemplateConfig] - The main configurations for webezy.io template",
                        "type": "object",
                        "properties": {
                            "name": {
                                "description": "[webezy.WebezyTemplate.v1.TemplateConfig.name] - The template name",
                                "type": "string"
                            },
                            "outPath": {
                                "description": "[webezy.WebezyTemplate.v1.TemplateConfig.out_path] - The output path for the template script",
                                "type": "string"
                            },
                            "include": {
                                "description": "[webezy.WebezyTemplate.v1.TemplateConfig.include] - The files to include when using 'include_code' field",
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "exclude": {
                                "description": "[webezy.WebezyTemplate.v1.TemplateConfig.exclude] - The files to exclude when using 'include_code' field",
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "tags": {
                                "description": "[webezy.WebezyTemplate.v1.TemplateConfig.tags] - The optional tags to associate with the template",
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "description": {
                                "description": "[webezy.WebezyTemplate.v1.TemplateConfig.description] - The template description",
                                "type": "string"
                            },
                            "author": {
                                "description": "[webezy.WebezyTemplate.v1.TemplateConfig.author] - The author email or name",
                                "type": "string"
                            },
                            "includeCode": {
                                "description": "[webezy.WebezyTemplate.v1.TemplateConfig.include_code] - If to include code files in the generated template script",
                                "type": "boolean"
                            }
                        },
                        "propertyOrder": [
                            "name",
                            "outPath",
                            "include",
                            "exclude",
                            "tags",
                            "description",
                            "author",
                            "includeCode"
                        ],
                        "required": [
                            "author",
                            "description",
                            "exclude",
                            "include",
                            "includeCode",
                            "name",
                            "outPath",
                            "tags"
                        ]
                    },
                    "WebezyMonitor": {
                        "description": "[webezy.WebezyConfig.v1.WebezyMonitor] - WebezyMonitor configurations",
                        "type": "object",
                        "properties": {
                            "prometheus": {
                                "description": "[webezy.WebezyConfig.v1.WebezyMonitor.prometheus] - The prometheus client configurations",
                                "$ref": "#/definitions/PrometheusConfig"
                            }
                        },
                        "propertyOrder": [
                            "prometheus"
                        ]
                    },
                    "PrometheusConfig": {
                        "description": "[webezy.WebezyPrometheus.v1.PrometheusConfig] - The prometheus description for configuration file",
                        "type": "object",
                        "properties": {
                            "globalConfig": {
                                "description": "[webezy.WebezyPrometheus.v1.PrometheusConfig.global_config] - The global configurations for prometheus",
                                "$ref": "#/definitions/GlobalConfig"
                            },
                            "scrapeConfigs": {
                                "description": "[webezy.WebezyPrometheus.v1.PrometheusConfig.scrape_configs] - The list of scrapes for prometheus",
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/ScrapeConfig"
                                }
                            }
                        },
                        "propertyOrder": [
                            "globalConfig",
                            "scrapeConfigs"
                        ],
                        "required": [
                            "scrapeConfigs"
                        ]
                    },
                    "GlobalConfig": {
                        "description": "[webezy.WebezyPrometheus.v1.GlobalConfig] - The prometheus global configs",
                        "type": "object",
                        "properties": {
                            "scrapeInterval": {
                                "description": "[webezy.WebezyPrometheus.v1.GlobalConfig.scrape_interval] - The global scrape interval in secondes",
                                "type": "number"
                            }
                        },
                        "propertyOrder": [
                            "scrapeInterval"
                        ],
                        "required": [
                            "scrapeInterval"
                        ]
                    },
                    "ScrapeConfig": {
                        "description": "[webezy.WebezyPrometheus.v1.ScrapeConfig] - The prometheus scrape specific configs",
                        "type": "object",
                        "properties": {
                            "jobName": {
                                "description": "[webezy.WebezyPrometheus.v1.ScrapeConfig.job_name] - The specified job name",
                                "type": "string"
                            },
                            "scrapeInterval": {
                                "description": "[webezy.WebezyPrometheus.v1.ScrapeConfig.scrape_interval] - The scrape interval for the specified job - in secondes",
                                "type": "number"
                            },
                            "staticConfigs": {
                                "description": "[webezy.WebezyPrometheus.v1.ScrapeConfig.static_configs] -",
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/StaticConfig"
                                }
                            }
                        },
                        "propertyOrder": [
                            "jobName",
                            "scrapeInterval",
                            "staticConfigs"
                        ],
                        "required": [
                            "jobName",
                            "scrapeInterval",
                            "staticConfigs"
                        ]
                    },
                    "StaticConfig": {
                        "description": "[webezy.WebezyPrometheus.v1.StaticConfig] - The static config specified for job",
                        "type": "object",
                        "properties": {
                            "targets": {
                                "description": "[webezy.WebezyPrometheus.v1.StaticConfig.targets] - The targets array consist of HOST:PORT value",
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "labels": {
                                "description": "[webezy.WebezyPrometheus.v1.StaticConfig.labels] -",
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/StaticConfigLabel"
                                }
                            }
                        },
                        "propertyOrder": [
                            "targets",
                            "labels"
                        ],
                        "required": [
                            "labels",
                            "targets"
                        ]
                    },
                    "StaticConfigLabel": {
                        "description": "[webezy.WebezyPrometheus.v1.StaticConfigLabel] - The label for the static config",
                        "type": "object",
                        "properties": {
                            "serviceName": {
                                "description": "[webezy.WebezyPrometheus.v1.StaticConfigLabel.service_name] - The service name",
                                "type": "string"
                            },
                            "group": {
                                "description": "[webezy.WebezyPrometheus.v1.StaticConfigLabel.group] - the group",
                                "type": "string"
                            }
                        },
                        "propertyOrder": [
                            "serviceName",
                            "group"
                        ],
                        "required": [
                            "group",
                            "serviceName"
                        ]
                    },
                    "WebezyService": {
                        "description": "[webezy.WebezyService.v1.WebezyService] - The webezy service descripiton",
                        "type": "object",
                        "properties": {
                            "uri": {
                                "description": "[webezy.WebezyService.v1.WebezyService.uri] - The service URI for the resource",
                                "type": "string"
                            },
                            "name": {
                                "description": "[webezy.WebezyService.v1.WebezyService.name] - Service name - MUST not hold any blank spaces and SHOULD be Capitalized CamelCased",
                                "type": "string"
                            },
                            "fullName": {
                                "description": "[webezy.WebezyService.v1.WebezyService.full_name] - The service full name consisting of - <domain>.<name>.<version>",
                                "type": "string"
                            },
                            "methods": {
                                "description": "[webezy.WebezyService.v1.WebezyService.methods] -",
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/WebezyMethod"
                                }
                            },
                            "version": {
                                "description": "[webezy.WebezyService.v1.WebezyService.version] -",
                                "type": "string"
                            },
                            "dependencies": {
                                "description": "[webezy.WebezyService.v1.WebezyService.dependencies] -",
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "description": {
                                "description": "[webezy.WebezyService.v1.WebezyService.description] -",
                                "type": "string"
                            },
                            "type": {
                                "description": "[webezy.WebezyService.v1.WebezyService.type] -",
                                "type": "string"
                            },
                            "kind": {
                                "description": "[webezy.WebezyService.v1.WebezyService.kind] -",
                                "type": "string"
                            },
                            "extensions": {
                                "description": "[webezy.WebezyService.v1.WebezyService.extensions] -",
                                "type": "object",
                                "additionalProperties": {},
                                "propertyOrder": []
                            }
                        },
                        "propertyOrder": [
                            "uri",
                            "name",
                            "fullName",
                            "methods",
                            "version",
                            "dependencies",
                            "description",
                            "type",
                            "kind",
                            "extensions"
                        ],
                        "required": [
                            "fullName",
                            "methods",
                            "name",
                            "type",
                            "uri",
                            "version"
                        ]
                    },
                    "WebezyMethod": {
                        "description": "[webezy.WebezyService.v1.WebezyMethod] - The webezy service method (RPC) description",
                        "type": "object",
                        "properties": {
                            "uri": {
                                "description": "[webezy.WebezyService.v1.WebezyMethod.uri] - The method URI",
                                "type": "string"
                            },
                            "name": {
                                "description": "[webezy.WebezyService.v1.WebezyMethod.name] - Method name",
                                "type": "string"
                            },
                            "fullName": {
                                "description": "[webezy.WebezyService.v1.WebezyMethod.full_name] - Method full name",
                                "type": "string"
                            },
                            "type": {
                                "description": "[webezy.WebezyService.v1.WebezyMethod.type] - The resource type",
                                "type": "string"
                            },
                            "kind": {
                                "description": "[webezy.WebezyService.v1.WebezyMethod.kind] - The resource kind",
                                "type": "string"
                            },
                            "inputType": {
                                "description": "[webezy.WebezyService.v1.WebezyMethod.input_type] - The full resource name (message full name) for input type",
                                "type": "string"
                            },
                            "outputType": {
                                "description": "[webezy.WebezyService.v1.WebezyMethod.output_type] - The full resource name (message full name) for output type",
                                "type": "string"
                            },
                            "clientStreaming": {
                                "description": "[webezy.WebezyService.v1.WebezyMethod.client_streaming] - If method is client stream flag",
                                "type": "boolean"
                            },
                            "serverStreaming": {
                                "description": "[webezy.WebezyService.v1.WebezyMethod.server_streaming] - If method is server stream flag",
                                "type": "boolean"
                            },
                            "description": {
                                "description": "[webezy.WebezyService.v1.WebezyMethod.description] - The method human readable description",
                                "type": "string"
                            },
                            "extensions": {
                                "description": "[webezy.WebezyService.v1.WebezyMethod.extensions] - The method (RPC) pluggable extensions configurations",
                                "type": "object",
                                "additionalProperties": {},
                                "propertyOrder": []
                            }
                        },
                        "propertyOrder": [
                            "uri",
                            "name",
                            "fullName",
                            "type",
                            "kind",
                            "inputType",
                            "outputType",
                            "clientStreaming",
                            "serverStreaming",
                            "description",
                            "extensions"
                        ],
                        "required": [
                            "inputType",
                            "kind",
                            "name",
                            "outputType",
                            "type",
                            "uri"
                        ]
                    },
                    "WebezyPackage": {
                        "description": "[webezy.WebezyPackage.v1.WebezyPackage] - The webezy package descriptor",
                        "type": "object",
                        "properties": {
                            "uri": {
                                "description": "[webezy.WebezyPackage.v1.WebezyPackage.uri] - Package URI",
                                "type": "string"
                            },
                            "name": {
                                "description": "[webezy.WebezyPackage.v1.WebezyPackage.name] - Package name",
                                "type": "string"
                            },
                            "package": {
                                "description": "[webezy.WebezyPackage.v1.WebezyPackage.package] - The package unique full name",
                                "type": "string"
                            },
                            "version": {
                                "description": "[webezy.WebezyPackage.v1.WebezyPackage.version] - Package version",
                                "type": "string"
                            },
                            "description": {
                                "description": "[webezy.WebezyPackage.v1.WebezyPackage.description] - Package human readable description",
                                "type": "string"
                            },
                            "type": {
                                "description": "[webezy.WebezyPackage.v1.WebezyPackage.type] - Package type",
                                "type": "string"
                            },
                            "kind": {
                                "description": "[webezy.WebezyPackage.v1.WebezyPackage.kind] - Pakcage king",
                                "type": "string"
                            },
                            "messages": {
                                "description": "[webezy.WebezyPackage.v1.WebezyPackage.messages] - The package messages array",
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/WebezyMessage"
                                }
                            },
                            "enums": {
                                "description": "[webezy.WebezyPackage.v1.WebezyPackage.enums] - The package enums array",
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/WebezyEnum"
                                }
                            },
                            "extensions": {
                                "description": "[webezy.WebezyPackage.v1.WebezyPackage.extensions] - The package pluggable extensions",
                                "type": "object",
                                "additionalProperties": {},
                                "propertyOrder": []
                            },
                            "dependencies": {
                                "description": "[webezy.WebezyPackage.v1.WebezyPackage.dependencies] -",
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            }
                        },
                        "propertyOrder": [
                            "uri",
                            "name",
                            "package",
                            "version",
                            "description",
                            "type",
                            "kind",
                            "messages",
                            "enums",
                            "extensions",
                            "dependencies"
                        ],
                        "required": [
                            "messages",
                            "name",
                            "package",
                            "type",
                            "uri",
                            "version"
                        ]
                    },
                    "WebezyMessage": {
                        "description": "[webezy.WebezyPackage.v1.WebezyMessage] - The webezy message descriptor",
                        "type": "object",
                        "properties": {
                            "uri": {
                                "description": "[webezy.WebezyPackage.v1.WebezyMessage.uri] - Message URI",
                                "type": "string"
                            },
                            "name": {
                                "description": "[webezy.WebezyPackage.v1.WebezyMessage.name] - Message name",
                                "type": "string"
                            },
                            "fullName": {
                                "description": "[webezy.WebezyPackage.v1.WebezyMessage.full_name] - Message full name <domain>.<package>.<version>.<message>",
                                "type": "string"
                            },
                            "fields": {
                                "description": "[webezy.WebezyPackage.v1.WebezyMessage.fields] - The fields array under the specified message type",
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/WebezyField"
                                }
                            },
                            "type": {
                                "description": "[webezy.WebezyPackage.v1.WebezyMessage.type] - Message type",
                                "type": "string"
                            },
                            "kind": {
                                "description": "[webezy.WebezyPackage.v1.WebezyMessage.kind] - Message kind",
                                "type": "string"
                            },
                            "description": {
                                "description": "[webezy.WebezyPackage.v1.WebezyMessage.description] - Human readable message description",
                                "type": "string"
                            },
                            "extensionType": {
                                "$ref": "#/definitions/WebezyExtension",
                                "description": "[webezy.WebezyPackage.v1.WebezyMessage.extension_type] - Optional if to extend this message"
                            },
                            "extensions": {
                                "description": "[webezy.WebezyPackage.v1.WebezyMessage.extensions] - A map of pluggable extensions into message",
                                "type": "object",
                                "additionalProperties": {},
                                "propertyOrder": []
                            }
                        },
                        "propertyOrder": [
                            "uri",
                            "name",
                            "fullName",
                            "fields",
                            "type",
                            "kind",
                            "description",
                            "extensionType",
                            "extensions"
                        ],
                        "required": [
                            "fields",
                            "fullName",
                            "kind",
                            "name",
                            "type",
                            "uri"
                        ]
                    },
                    "WebezyField": {
                        "description": "[webezy.WebezyPackage.v1.WebezyField] - The webezy field descriptor",
                        "type": "object",
                        "properties": {
                            "uri": {
                                "description": "[webezy.WebezyPackage.v1.WebezyField.uri] - The field URI",
                                "type": "string"
                            },
                            "name": {
                                "description": "[webezy.WebezyPackage.v1.WebezyField.name] - The field name",
                                "type": "string"
                            },
                            "fullName": {
                                "description": "[webezy.WebezyPackage.v1.WebezyField.full_name] - The field full name <domain>.<package>.<version>.<message>.<field>",
                                "type": "string"
                            },
                            "index": {
                                "description": "[webezy.WebezyPackage.v1.WebezyField.index] - The field index at the message level hierarchy",
                                "type": "number"
                            },
                            "fieldType": {
                                "$ref": "#/definitions/WebezyFieldType",
                                "description": "[webezy.WebezyPackage.v1.WebezyField.field_type] - The field type"
                            },
                            "label": {
                                "$ref": "#/definitions/WebezyFieldLabel",
                                "description": "[webezy.WebezyPackage.v1.WebezyField.label] - The field label"
                            },
                            "enumType": {
                                "description": "[webezy.WebezyPackage.v1.WebezyField.enum_type] - If field is type ENUM this field MUST be populated with full resource name of the ENUM",
                                "type": "string"
                            },
                            "messageType": {
                                "description": "[webezy.WebezyPackage.v1.WebezyField.message_type] - If the field type is of type MESSAGE then this field MUST be populated with the full resource name of the MESSAGE",
                                "type": "string"
                            },
                            "type": {
                                "description": "[webezy.WebezyPackage.v1.WebezyField.type] - The message resource type",
                                "type": "string"
                            },
                            "kind": {
                                "description": "[webezy.WebezyPackage.v1.WebezyField.kind] - The message resource kind",
                                "type": "string"
                            },
                            "description": {
                                "description": "[webezy.WebezyPackage.v1.WebezyField.description] - The field human readable description",
                                "type": "string"
                            },
                            "keyType": {
                                "$ref": "#/definitions/WebezyFieldType",
                                "description": "[webezy.WebezyPackage.v1.WebezyField.key_type] - If field is of type MAP then this field MUST be populated with the map< KEY,> type"
                            },
                            "valueType": {
                                "$ref": "#/definitions/WebezyFieldType",
                                "description": "[webezy.WebezyPackage.v1.WebezyField.value_type] - If field is of type MAP then this field MUST be populated with the map<, VALUE> type"
                            },
                            "extensions": {
                                "description": "[webezy.WebezyPackage.v1.WebezyField.extensions] - The field extensions",
                                "type": "object",
                                "additionalProperties": {},
                                "propertyOrder": []
                            },
                            "oneofFields": {
                                "description": "[webezy.WebezyPackage.v1.WebezyField.oneof_fields] -",
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/WebezyOneOfField"
                                }
                            }
                        },
                        "propertyOrder": [
                            "uri",
                            "name",
                            "fullName",
                            "index",
                            "fieldType",
                            "label",
                            "enumType",
                            "messageType",
                            "type",
                            "kind",
                            "description",
                            "keyType",
                            "valueType",
                            "extensions",
                            "oneofFields"
                        ],
                        "required": [
                            "fieldType",
                            "fullName",
                            "index",
                            "kind",
                            "label",
                            "name",
                            "type",
                            "uri"
                        ]
                    },
                    "WebezyFieldType": {
                        "description": "[webezy.WebezyPackage.v1.WebezyFieldType] - None",
                        "enum": [
                            -1,
                            "UNKNOWN_WEBEZYFIELDTYPE",
                            "TYPE_DOUBLE",
                            "TYPE_FLOAT",
                            "TYPE_INT64",
                            "TYPE_UINT64",
                            "TYPE_INT32",
                            "TYPE_BOOL",
                            "TYPE_STRING",
                            "TYPE_MESSAGE",
                            "TYPE_BYTES",
                            "TYPE_ENUM",
                            "TYPE_MAP",
                            "TYPE_ONEOF"
                        ],
                        "type": "string"
                    },
                    "WebezyFieldLabel": {
                        "description": "[webezy.WebezyPackage.v1.WebezyFieldLabel] - None",
                        "enum": [
                            "UNKNOWN_WEBEZYFIELDLABEL",
                            "LABEL_OPTIONAL",
                            "LABEL_REPEATED"
                        ],
                        "type": "string"
                    },
                    "WebezyOneOfField": {
                        "description": "[webezy.WebezyPackage.v1.WebezyOneOfField] - None",
                        "type": "object",
                        "properties": {
                            "uri": {
                                "description": "[webezy.WebezyPackage.v1.WebezyOneOfField.uri] -",
                                "type": "string"
                            },
                            "name": {
                                "description": "[webezy.WebezyPackage.v1.WebezyOneOfField.name] -",
                                "type": "string"
                            },
                            "fullName": {
                                "description": "[webezy.WebezyPackage.v1.WebezyOneOfField.full_name] -",
                                "type": "string"
                            },
                            "index": {
                                "description": "[webezy.WebezyPackage.v1.WebezyOneOfField.index] -",
                                "type": "number"
                            },
                            "enumType": {
                                "description": "[webezy.WebezyPackage.v1.WebezyOneOfField.enum_type] -",
                                "type": "string"
                            },
                            "messageType": {
                                "description": "[webezy.WebezyPackage.v1.WebezyOneOfField.message_type] -",
                                "type": "string"
                            },
                            "type": {
                                "description": "[webezy.WebezyPackage.v1.WebezyOneOfField.type] -",
                                "type": "string"
                            },
                            "kind": {
                                "description": "[webezy.WebezyPackage.v1.WebezyOneOfField.kind] -",
                                "type": "string"
                            },
                            "description": {
                                "description": "[webezy.WebezyPackage.v1.WebezyOneOfField.description] -",
                                "type": "string"
                            },
                            "extensions": {
                                "description": "[webezy.WebezyPackage.v1.WebezyOneOfField.extensions] - A map of pluggable extensions into field",
                                "type": "object",
                                "additionalProperties": {},
                                "propertyOrder": []
                            }
                        },
                        "propertyOrder": [
                            "uri",
                            "name",
                            "fullName",
                            "index",
                            "enumType",
                            "messageType",
                            "type",
                            "kind",
                            "description",
                            "extensions"
                        ],
                        "required": [
                            "fullName",
                            "index",
                            "kind",
                            "name",
                            "type",
                            "uri"
                        ]
                    },
                    "WebezyExtension": {
                        "description": "[webezy.WebezyPackage.v1.WebezyExtension] - None",
                        "enum": [
                            "UNKNOWN_WEBEZYEXTENSION",
                            "FileOptions",
                            "MessageOptions",
                            "FieldOptions",
                            "ServiceOptions",
                            "MethodOptions"
                        ],
                        "type": "string"
                    },
                    "WebezyEnum": {
                        "description": "[webezy.WebezyPackage.v1.WebezyEnum] - The webezy enum descriptor",
                        "type": "object",
                        "properties": {
                            "uri": {
                                "description": "[webezy.WebezyPackage.v1.WebezyEnum.uri] - Enum URI",
                                "type": "string"
                            },
                            "name": {
                                "description": "[webezy.WebezyPackage.v1.WebezyEnum.name] - Enum name",
                                "type": "string"
                            },
                            "fullName": {
                                "description": "[webezy.WebezyPackage.v1.WebezyEnum.full_name] - Enum full name <domain>.<package>.<version>.<enum>",
                                "type": "string"
                            },
                            "values": {
                                "description": "[webezy.WebezyPackage.v1.WebezyEnum.values] - Array of enum value",
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/WebezyEnumValue"
                                }
                            },
                            "type": {
                                "description": "[webezy.WebezyPackage.v1.WebezyEnum.type] - Enum type",
                                "type": "string"
                            },
                            "kind": {
                                "description": "[webezy.WebezyPackage.v1.WebezyEnum.kind] - Enum kind",
                                "type": "string"
                            },
                            "description": {
                                "description": "[webezy.WebezyPackage.v1.WebezyEnum.description] - Enum human readable description",
                                "type": "string"
                            }
                        },
                        "propertyOrder": [
                            "uri",
                            "name",
                            "fullName",
                            "values",
                            "type",
                            "kind",
                            "description"
                        ],
                        "required": [
                            "fullName",
                            "kind",
                            "name",
                            "type",
                            "uri",
                            "values"
                        ]
                    },
                    "WebezyEnumValue": {
                        "description": "[webezy.WebezyPackage.v1.WebezyEnumValue] - The webezy enum value descriptor",
                        "type": "object",
                        "properties": {
                            "uri": {
                                "description": "[webezy.WebezyPackage.v1.WebezyEnumValue.uri] - Enum value URI",
                                "type": "string"
                            },
                            "name": {
                                "description": "[webezy.WebezyPackage.v1.WebezyEnumValue.name] - Enum value name",
                                "type": "string"
                            },
                            "number": {
                                "description": "[webezy.WebezyPackage.v1.WebezyEnumValue.number] - Enum value number (value)",
                                "type": "number"
                            },
                            "index": {
                                "description": "[webezy.WebezyPackage.v1.WebezyEnumValue.index] - The enum value index at the enum values array",
                                "type": "number"
                            },
                            "type": {
                                "description": "[webezy.WebezyPackage.v1.WebezyEnumValue.type] - Enum value type",
                                "type": "string"
                            },
                            "kind": {
                                "description": "[webezy.WebezyPackage.v1.WebezyEnumValue.kind] - Enum value kind",
                                "type": "string"
                            },
                            "description": {
                                "description": "[webezy.WebezyPackage.v1.WebezyEnumValue.description] - Human readable description for the enum value",
                                "type": "string"
                            }
                        },
                        "propertyOrder": [
                            "uri",
                            "name",
                            "number",
                            "index",
                            "type",
                            "kind",
                            "description"
                        ],
                        "required": [
                            "kind",
                            "name",
                            "type",
                            "uri"
                        ]
                    }
                },
                "$schema": "http://json-schema.org/draft-07/schema#"
            }
        }
    ]
}
```