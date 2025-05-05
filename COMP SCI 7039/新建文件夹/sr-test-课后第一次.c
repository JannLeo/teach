#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include "emulator.h"
#include "sr.h"
#include <string.h>

/* ******************************************************************
   Go Back N protocol.  Adapted from J.F.Kurose
   ALTERNATING BIT AND GO-BACK-N NETWORK EMULATOR: VERSION 1.2  

   Network properties:
   - one way network delay averages five time units (longer if there
   are other messages in the channel for GBN), but can be larger
   - packets can be corrupted (either the header or the data portion)
   or lost, according to user-defined probabilities
   - packets will be delivered in the order in which they were sent
   (although some can be lost).

   Modifications: 
   - removed bidirectional GBN code and other code not used by prac. 
   - fixed C style to adhere to current programming style
   - added GBN implementation
**********************************************************************/

#define RTT  16.0       /* round trip time.  MUST BE SET TO 16.0 when submitting assignment */
#define WINDOWSIZE 6    /* the maximum number of buffered unacked packet */
#define SEQSPACE 7      /* the min sequence space for GBN must be at least windowsize + 1 */
#define NOTINUSE (-1)   /* used to fill header fields that are not being used */

/* generic procedure to compute the checksum of a packet.  Used by both sender and receiver  
   the simulator will overwrite part of your packet with 'z's.  It will not overwrite your 
   original checksum.  This procedure must generate a different checksum to the original if
   the packet is corrupted.
*/

#define RECV_WINDOWSIZE 6

static struct pkt buffered[RECV_WINDOWSIZE];
static int recv_base;
static bool received[RECV_WINDOWSIZE];
static bool acked[SEQSPACE];

int ComputeChecksum(struct pkt packet)
{
  int checksum = 0;
  int i;

  checksum = packet.seqnum;
  checksum += packet.acknum;
  for ( i=0; i<20; i++ ) 
    checksum += (int)(packet.payload[i]);

  return checksum;
}

bool IsCorrupted(struct pkt packet)
{
  if (packet.checksum == ComputeChecksum(packet))
    return (false);
  else
    return (true);
}

static struct pkt buffer[SEQSPACE];
static int window_base = 0;
static int windowcount;
static int A_nextseqnum;
static int current_timer_seq = -1;

/* called from layer 5 (application layer), passed the message to be sent to other side */
void A_output(struct msg message)
{
    struct pkt sendpkt;
    int i;

    if (windowcount < WINDOWSIZE) {
        if (TRACE > 1)
        printf("----A: New message arrives, send window is not full, send new messge to layer3!\n");

        sendpkt.seqnum = A_nextseqnum;
        sendpkt.acknum = NOTINUSE;
        for ( i=0; i<20 ; i++ ) 
            sendpkt.payload[i] = message.data[i];
        sendpkt.checksum = ComputeChecksum(sendpkt);

        buffer[sendpkt.seqnum] = sendpkt;
        acked[sendpkt.seqnum] = false;
        windowcount++;

        if (TRACE > 0)
            printf("Sending packet %d to layer 3\n", sendpkt.seqnum);
        tolayer3(A, sendpkt);

        if (windowcount == 1) {
            current_timer_seq = sendpkt.seqnum;
            starttimer(A, RTT);
        }
        A_nextseqnum = (A_nextseqnum + 1) % SEQSPACE;  
    } else {
        if (TRACE > 0)
            printf("----A: New message arrives, send window is full\n");
        window_full++;
    }
}

void StartTimerForNextUnackedPacket() {
    int i;
    for (i = 0; i < SEQSPACE; i++) {
        int seq = (window_base + i) % SEQSPACE;
        if (!acked[seq] && i < windowcount) {
            current_timer_seq = seq;
            starttimer(A, RTT);
            if (TRACE > 2)
                printf("----A: start timer for packet %d\n", seq);
            break;
        }
    }
}

void StopTimerIfAcked(int acknum) {
    if (acknum == current_timer_seq) {
        if (TRACE > 2)
            printf("----A: stopping timer for packet %d\n", acknum);
        stoptimer(A);
        current_timer_seq = -1;
        StartTimerForNextUnackedPacket();
    }
}

/* called from layer 3, when a packet arrives for layer 4 
   In this practical this will always be an ACK as B never sends data.
*/
void A_input(struct pkt packet)
{
    int win_start;
    int win_end;
    bool in_window;
    
    if (!IsCorrupted(packet)) {
        if (TRACE > 0)
            printf("----A: uncorrupted ACK %d is received\n", packet.acknum);
        total_ACKs_received++;

        win_start = window_base;
        win_end = (window_base + WINDOWSIZE) % SEQSPACE;
        in_window = (win_start < win_end) ?
                         (packet.acknum >= win_start && packet.acknum < win_end) :
                         (packet.acknum >= win_start || packet.acknum < win_end);

        if (!in_window) {
            if (TRACE > 2)
                printf("----A: ACK %d is outside window [%d, %d), ignored\n", packet.acknum, win_start, win_end);
            return;
        }

        if (!acked[packet.acknum]) {
            if (TRACE > 0)
                printf("----A: ACK %d is not a duplicate\n", packet.acknum);
            acked[packet.acknum] = true;
            new_ACKs++;
            StopTimerIfAcked(packet.acknum);

            while (windowcount > 0 && acked[window_base]) {
                acked[window_base] = false;
                window_base = (window_base + 1) % SEQSPACE;
                windowcount--;
            }
        } else {
            if (TRACE > 0)
                printf("----A: duplicate ACK received, do nothing!\n");
        }
    } else {
        if (TRACE > 0)
            printf("----A: corrupted ACK is received, do nothing!\n");
    }
}

/* called when A's timer goes off */
void A_timerinterrupt(void)
{
    if (TRACE > 0)
        printf("----A: time out, resend packets!\n");

    if (!acked[current_timer_seq]) {
        if (TRACE > 0)
            printf("---A: resending packet %d\n", buffer[current_timer_seq].seqnum);
        tolayer3(A, buffer[current_timer_seq]);
        packets_resent++;
    }
    StartTimerForNextUnackedPacket();
}

/* the following routine will be called once (only) before any other */
/* entity A routines are called. You can use it to do any initialization */
void A_init(void)
{
    int i;
  /* initialise A's window, buffer and sequence number */
  A_nextseqnum = 0;  /* A starts with seq num 0, do not change this */
  windowcount = 0;

  for (i = 0; i < SEQSPACE; i++) {
        acked[i] = false;
    }
}

/********* Receiver (B)  variables and procedures ************/

/*static int expectedseqnum; *//* the sequence number expected next by the receiver */
static int B_nextseqnum;

bool IsInWindow(int seqnum, int base, int size) {
    int end = (base + size) % SEQSPACE;
    if (base < end)
        return (seqnum >= base && seqnum < end);
    else
        return (seqnum >= base || seqnum < end);
}

bool IsBeforeWindow(int seqnum, int base) {
    int diff = (seqnum - base + SEQSPACE) % SEQSPACE;
    return diff >= SEQSPACE - RECV_WINDOWSIZE;
}

int CalculateBufferIndex(int seqnum) {
    return (seqnum - recv_base + SEQSPACE) % SEQSPACE;
}



/* called from layer 3, when a packet arrives for layer 4 at B*/
/* called from layer 3, when a packet arrives for layer 4 at B */
void B_input(struct pkt packet)
{
    struct pkt sendpkt;
    int i;
    int seqnum = packet.seqnum;
    int bufferIndex;

    sendpkt.seqnum = B_nextseqnum;
    B_nextseqnum = (B_nextseqnum + 1) % 2;


    for (i = 0; i < 20; i++) {
        sendpkt.payload[i] = '0';
    }
        
    if (IsCorrupted(packet)) {
        if (TRACE > 0)
            printf("----B: packet corrupted or not expected sequence number, resend ACK!\n");
        sendpkt.acknum = (recv_base + SEQSPACE - 1) % SEQSPACE;
        sendpkt.checksum = ComputeChecksum(sendpkt);
        tolayer3(B, sendpkt);
        return;
    }

    if (IsInWindow(seqnum, recv_base, RECV_WINDOWSIZE)) {
        bufferIndex = (seqnum - recv_base + SEQSPACE) % SEQSPACE;

        if (!received[bufferIndex]) {
            buffered[bufferIndex] = packet;
            received[bufferIndex] = true;
            packets_received++;
            if (TRACE > 0)
                printf("----B: packet %d is correctly received and buffered\n", seqnum);
        }

        bufferIndex = CalculateBufferIndex(recv_base);
        while (received[bufferIndex]) {
            tolayer5(B, buffered[bufferIndex].payload);
            received[bufferIndex] = false;
            recv_base = (recv_base + 1) % SEQSPACE;
            if (TRACE > 2)
                printf("----B: window slides to %d\n", recv_base);
            bufferIndex = CalculateBufferIndex(recv_base);
        }

        sendpkt.acknum = seqnum;
    }
    else if (IsBeforeWindow(seqnum, recv_base)) {
        if (TRACE > 2)
            printf("----B: received old packet %d, resend ACK\n", seqnum);
        sendpkt.acknum = seqnum;
    }
    else {
        if (TRACE > 2)
            printf("----B: packet %d outside receive window, ignored\n", seqnum);
        return;
    }
    sendpkt.checksum = ComputeChecksum(sendpkt);
    tolayer3(B, sendpkt);
}

/* the following routine will be called once (only) before any other */
/* entity B routines are called. You can use it to do any initialization */
void B_init(void)
{
    int i;
    recv_base = 0;
    B_nextseqnum = 1;

    for (i = 0; i < RECV_WINDOWSIZE; i++) {
        received[i] = false;
    }
}

/******************************************************************************
 * The following functions need be completed only for bi-directional messages *
 *****************************************************************************/

/* Note that with simplex transfer from a-to-B, there is no B_output() */
void B_output(struct msg message)  
{
}

/* called when B's timer goes off */
void B_timerinterrupt(void)
{
}