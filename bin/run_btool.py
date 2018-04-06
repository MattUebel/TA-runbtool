import sys
import os
import subprocess
import itertools
import re

from splunklib.searchcommands import dispatch, GeneratingCommand, Configuration, Option, validators

@Configuration(streaming=False, local=True, type='reporting')
class runBtool(GeneratingCommand):
    confFile = Option(require=True)
    searchPeer = Option(require=False)
    splunk_exe = os.path.join(os.environ['SPLUNK_HOME'], 'bin', 'splunk')

    def generate(self):
        valid_files = ['alert_actions','app','audit','authentication','authorize','checklist','collections','commands','datamodels','datatypesbnf','default-mode','deployment','deploymentclient','distsearch','eventdiscoverer','event_renderers','eventtypes','fields','indexes','inputs','limits','literals','macros','messages','multikv','outputs','passwords','procmon-filters','props','pubsub','restmap','savedsearches','searchbnf','segmenters','server','serverclass','source-classifier','sourcetypes','tags','telemetry','times','transactiontypes','transforms','ui-prefs','ui-tour','user-prefs','viewstates','visualizations','web','wmi','workflow_actions']
        if self.confFile not in valid_files:
            for i in valid_files:
                yield {'valid_file_names': i}
        else:
            try:
                if self.searchPeer is not None:
                    peerString = '--peername=' + self.searchPeer
                    
                    confFileOutput = subprocess.check_output([self.splunk_exe, 'btool', '--debug', self.confFile, 'list', peerString])
                    
                    directiveOutput = subprocess.check_output([self.splunk_exe, 'btool', self.confFile, 'list', peerString])
                    
                    stanzaOutput = subprocess.check_output([self.splunk_exe, 'btool', '--debug-print=stanza', self.confFile, 'list', peerString])
                else:                        
                    confFileOutput = subprocess.check_output([self.splunk_exe, 'btool', '--debug', self.confFile, 'list'])
                    
                    directiveOutput = subprocess.check_output([self.splunk_exe, 'btool', self.confFile, 'list'])
                    
                    stanzaOutput = subprocess.check_output([self.splunk_exe, 'btool', '--debug-print=stanza', self.confFile, 'list'])
        
                for j, k, l in itertools.izip_longest(confFileOutput.split('\n'), stanzaOutput.split('\n'), directiveOutput.split('\n')):
                    d_split = l.split('=')
                    d_name = d_split[0]
                    if len(d_split) == 2:
                        d_value = d_split[1]
                    elif len(d_split) == 1:
                        d_value = None
                    else:
                        d_value = "=".join(d_split[1:])
                    yield {'confFileLocation':re.compile("(?<=(\.conf))\s+").split(j)[0], 'stanza':re.compile("\s").split(k)[0], 'directiveName':d_name, 'directiveValue':d_value}
            except Exception as e:
                error = repr(e)
                yield {"error":error}

dispatch(runBtool, sys.argv, sys.stdin, sys.stdout, __name__)
