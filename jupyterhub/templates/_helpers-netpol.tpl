{{- define "jupyterhub.networkPolicy.standardEgressConfiguration" -}}
{{- include "jupyterhub.networkPolicy.standardEgressConfiguration.withLeadingNewLine" . | trimPrefix "\n" }}
{{- end }}

{{- define "jupyterhub.networkPolicy.standardEgressConfiguration.withLeadingNewLine" -}}
{{- $root := index . 0 }}
{{- $netpol := index . 1 }}
{{- if and ($netpol.egressAllowRules.dnsPortsPrivateIPs) (not $netpol.egressAllowRules.privateIPs) }}
# Allow outbound connections to the DNS port in the private IP ranges
- ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
  to:
    - ipBlock:
        cidr: 10.0.0.0/8
    - ipBlock:
        cidr: 172.16.0.0/12
    - ipBlock:
        cidr: 192.168.0.0/16
{{- end }}

{{- if $netpol.egressAllowRules.nonPrivateIPs }}
# Allow outbound connections to non-private IP ranges
{{- if $netpol.egressAllowRules.privateIPs }}
# Allow outbound connections to private IP ranges (and their DNS ports)
{{- end }}
{{- if $netpol.egressAllowRules.cloudMetadataServer }}
# Allow outbound connections to cloud metadata server
{{- end }}
- to:
    - ipBlock:
        cidr: 0.0.0.0/0
        {{- if or (not $netpol.egressAllowRules.privateIPs) (not $netpol.egressAllowRules.cloudMetadataServer) }}
        except:
          {{- if not $netpol.egressAllowRules.privateIPs }}
          # Don't allow outbound connections to private IP ranges
          - 10.0.0.0/8
          - 172.16.0.0/12
          - 192.168.0.0/16
          {{- end }}

          {{- if not $netpol.egressAllowRules.cloudMetadataServer }}
          # Don't allow access to the cloud metadata server
          - {{ $root.Values.singleuser.cloudMetadata.ip }}/32
          {{- end }}
        {{- end }}
{{- end }}

{{- if and ($netpol.egressAllowRules.privateIPs) (not $netpol.egressAllowRules.nonPrivateIPs) }}
# Allow outbound connections to private IP ranges (and their DNS ports)
- to:
    - ipBlock:
        cidr: 10.0.0.0/8
    - ipBlock:
        cidr: 172.16.0.0/12
    - ipBlock:
        cidr: 192.168.0.0/16
{{- end }}

{{- if and ($netpol.egressAllowRules.cloudMetadataServer) (not $netpol.egressAllowRules.nonPrivateIPs) }}
# Allow outbound connections to cloud metadata server
- to:
    - ipBlock:
        cidr: {{ $root.Values.singleuser.cloudMetadata.ip }}/32
{{- end }}

{{- with $netpol.egress }}
# Allow outbound connections based on user specified rules
{{- . | toYaml }}
{{- end }}
{{- end }}
