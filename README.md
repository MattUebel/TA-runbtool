# TA-runbtool

Author: Matt Uebel (muebel)
Email: matt.uebel@gmail.com

## Overview

This is a custom search command that runs the splunk command-line utility "btool" against the local system. The results are presented as a table format, with a list of dictionaries containing each config file location, name of directive, value of directive, and stanza name.

btool is not officially supported by Splunk, and in some cases can behave in somewhat wonky ways, but is generally a good tool to use when troubleshooting the configuration that exists on disk. This is distinct from the current running configuration that can be retrieved through the rest API for Splunk.

For any production environments, you will want to limit this search command to administrative users as it potentially allows web user access to sensitive information. This command is restricted to the `admin` role by default.

## Dependencies

* Tested on Splunk 6.6+, likely works on earlier versions
* Supported on Unix / Linux. Support for Windows coming

## Setup

* Install at $SPLUNK_HOME/etc/apps
* Restart Splunk

## Using

General usage is:

    | runbtool confFile=<CONFFILE> [searchPeer=<PEERNAME>]

`searchPeer` is optional. Somewhat unintuitively, this flag and will run btool against a config bundle in `$SPLUNK_HOME/var/run/searchpeers/PEERNAME`, and not against a remote system the system is peered with.

`confFile` is the configuration specification you'd like to interrogate. The full list is:

```'alert_actions','app','audit','authentication','authorize','checklist','collections','commands','datamodels','datatypesbnf','default-mode','deployment','deploymentclient','distsearch','eventdiscoverer','event_renderers','eventtypes','fields','indexes','inputs','limits','literals','macros','messages','multikv','outputs','passwords','procmon-filters','props','pubsub','restmap','savedsearches','searchbnf','segmenters','server','serverclass','source-classifier','sourcetypes','tags','telemetry','times','transactiontypes','transforms','ui-prefs','ui-tour','user-prefs','viewstates','visualizations','web','wmi','workflow_actions'```
