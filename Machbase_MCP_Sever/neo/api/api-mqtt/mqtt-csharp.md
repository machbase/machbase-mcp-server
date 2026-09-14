# Machbase Neo MQTT C# Client

## 준비

### dotnet-sdk 설치

```sh
brew install dotnet-sdk
```

### 프로젝트 디렉터리 생성

```sh
mkdir csharp-mqtt && cd csharp-mqtt
```

### 콘솔 프로젝트 생성

```sh
dotnet new console --framework net7.0
```

### MQTTnet 패키지 추가

```sh
dotnet add package MQTTnet --version 4.3.3.952
```

## 접속 (비 TLS)

MQTT 일반 소켓으로 machbase-neo에 접속합니다.

```c#
var mqttFactory = new MqttFactory();
var mqttClient = mqttFactory.CreateMqttClient();
var connectOptions = new MqttClientOptionsBuilder().WithTcpServer("127.0.0.1", 5653).Build();
var connAck = await mqttClient.ConnectAsync(connectOptions, CancellationToken.None);

connAck.DumpToConsole();
```

## 접속 종료

```c#
var mqttClientDisconnectOptions = mqttFactory.CreateClientDisconnectOptionsBuilder().Build();
await mqttClient.DisconnectAsync(mqttClientDisconnectOptions, CancellationToken.None);
```

## 메시지 발행

```c#
var msg = new MqttApplicationMessageBuilder()
.WithTopic("db/append/example")
.WithPayload(@"[
                [""temperature"",1677033057000000000,21.1],
                [""humidity"",1677033057000000000,0.53]
            ]")
.Build();

await mqttClient.PublishAsync(msg, CancellationToken.None);
```

## 전체 소스 코드

```c#
using MQTTnet;
using MQTTnet.Client;
using System.Text.Json;

namespace MqttTest
{
    internal class Program
    {
        private static async Task Main()
        {
            var mqttFactory = new MqttFactory();
            var mqttClient = mqttFactory.CreateMqttClient();
            var connectOptions = new MqttClientOptionsBuilder().WithTcpServer("127.0.0.1", 5653).Build();
            var connAck = await mqttClient.ConnectAsync(connectOptions, CancellationToken.None);
            
            connAck.DumpToConsole();

            var msg = new MqttApplicationMessageBuilder()
                .WithTopic("db/append/example")
                .WithPayload(@"[
                                [""temperature"",1677033057000000000,21.1],
                                [""humidity"",1677033057000000000,0.53]
                            ]")
                .Build();

            await mqttClient.PublishAsync(msg, CancellationToken.None);

            var mqttClientDisconnectOptions = mqttFactory.CreateClientDisconnectOptionsBuilder().Build();
            await mqttClient.DisconnectAsync(mqttClientDisconnectOptions, CancellationToken.None);
        }
    }
}

internal static class ObjectExtensions
{
    public static TObject DumpToConsole<TObject>(this TObject @object)
    {
        var output = "NULL";
        if (@object != null)
        {
            output = JsonSerializer.Serialize(@object, new JsonSerializerOptions
            {
                WriteIndented = true
            });
        }
        
        Console.WriteLine($"[{@object?.GetType().Name}]:\r\n{output}");
        return @object;
    }
}
```
