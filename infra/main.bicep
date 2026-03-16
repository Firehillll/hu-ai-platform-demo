// Azure Infrastructure — HU AI Platform
// Deploy: az deployment group create -g hu-ai-platform-rg -f infra/main.bicep

targetScope = 'resourceGroup'

@description('Environment name')
param environment string = 'dev'

@description('Azure region')
param location string = resourceGroup().location

@description('OpenAI model deployment name')
param openaiModelName string = 'gpt-4o'

var prefix = 'hu-ai-${environment}'

module keyVault 'modules/key-vault.bicep' = {
  name: '${prefix}-kv'
  params: {
    name: '${prefix}-kv'
    location: location
  }
}

module openai 'modules/openai.bicep' = {
  name: '${prefix}-openai'
  params: {
    name: '${prefix}-openai'
    location: location
    modelName: openaiModelName
  }
}

module aiSearch 'modules/ai-search.bicep' = {
  name: '${prefix}-search'
  params: {
    name: '${prefix}-search'
    location: location
  }
}

module monitoring 'modules/monitoring.bicep' = {
  name: '${prefix}-monitoring'
  params: {
    name: '${prefix}-monitoring'
    location: location
  }
}

module containerApp 'modules/container-app.bicep' = {
  name: '${prefix}-app'
  params: {
    name: '${prefix}-app'
    location: location
    openaiEndpoint: openai.outputs.endpoint
    searchEndpoint: aiSearch.outputs.endpoint
    appInsightsConnectionString: monitoring.outputs.connectionString
  }
}

output appUrl string = containerApp.outputs.url
