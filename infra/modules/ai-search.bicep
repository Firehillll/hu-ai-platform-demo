@description('Azure AI Search resource name')
param name string

@description('Azure region')
param location string

resource search 'Microsoft.Search/searchServices@2024-03-01-preview' = {
  name: name
  location: location
  sku: {
    name: 'basic'
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
  }
}

output endpoint string = 'https://${name}.search.windows.net'
output id string = search.id
