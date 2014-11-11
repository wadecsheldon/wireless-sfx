#include <SPI.h>         // needed for Arduino versions later than 0018
#include <Ethernet.h>
#include <EthernetUdp.h>         // UDP library from: bjoern@cs.stanford.edu 12/30/2008


// Enter a MAC address and IP address for your controller below.
// The IP address will be dependent on your local network:
byte mac[] = {  
  0xDE, 0x01, 0x23, 0x45, 0x67, 0x89 };
IPAddress broadcastip(255, 255, 255, 255);

unsigned int localPort = 9001;      // local port to listen on

// buffers for receiving and sending data
char  ReplyBuffer[] = "sfx_scan";       // a string to send back

// An EthernetUDP instance to let us send and receive packets over UDP
EthernetUDP Udp;

void setup() {
  // start the Ethernet and UDP:
  Ethernet.begin(mac);
  Udp.begin(localPort);
}

void loop() {
  
    Udp.beginPacket(broadcastip, localPort);
    Udp.write(ReplyBuffer);
    Udp.endPacket();
    delay(5000);
}
