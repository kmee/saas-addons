{{/* Expand the name of the chart */}}
{{- define "erplivre14-odoo-hml.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "erplivre14-odoo-hml.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/* Create chart name and version as used by the chart label */}}
{{- define "erplivre14-odoo-hml.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* Common labels */}}
{{- define "erplivre14-odoo-hml.labels" -}}
helm.sh/chart: {{ include "erplivre14-odoo-hml.chart" . }}
{{ include "erplivre14-odoo-hml.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/* Selector labels */}}
{{- define "erplivre14-odoo-hml.selectorLabels" -}}
{{- $chartFull := printf "%s-%s" .Chart.Name .Chart.AppVersion -}}
app.kubernetes.io/name: {{ include "erplivre14-odoo-hml.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: Helm
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
helm.sh/chart: {{ $chartFull }}
{{/* Odoo */}}
cattle.io/creator: norman
app: {{ include "erplivre14-odoo-hml.fullname" . }}
tier: {{ include "erplivre14-odoo-hml.fullname" . }}
{{- end }}


{{/* Create the name of the service account to use */}}
{{- define "erplivre14-odoo-hml.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "erplivre14-odoo-hml.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}


{{/* SMTP - Name */}}
{{- define "erplivre14-odoo-hml.mailName" -}}
{{- default .Values.smtp.name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* SMTP - Fullname */}}
{{- define "erplivre14-odoo-hml.mailFullname" -}}
{{- if .Values.smtp.name }}
{{- .Values.smtp.name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Values.smtp.name .Chart.Name }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/* SMTP - Selector labels */}}
{{- define "erplivre14-odoo-hml.mailSelectorLabels" -}}
app.kubernetes.io/name: {{ include "erplivre14-odoo-hml.mailName" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app: {{ include "erplivre14-odoo-hml.mailFullname" . }}
{{- end }}

{{/* SMTP - Service Account Name */}}
{{- define "erplivre14-odoo-hml.mailServiceAccountName" -}}
{{- default "default" .Values.smtp.name }}
{{- end }}

{{/* SMTP - Labels */}}
{{- define "erplivre14-odoo-hml.mailLabels" -}}
helm.sh/chart: {{ include "erplivre14-odoo-hml.chart" . }}
{{ include "erplivre14-odoo-hml.mailSelectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}