export class AudioRecorder {
    private mediaRecorder: MediaRecorder | null;
    private audioChunks: Blob[];
    private stream: MediaStream | null;
    private readonly sampleRate: number = 16000;
  
    constructor() {
      this.mediaRecorder = null;
      this.audioChunks = [];
      this.stream = null;
    }
  
    async initialize(): Promise<boolean> {
      try {
        this.stream = await navigator.mediaDevices.getUserMedia({
          audio: {
            channelCount: 1,
            sampleRate: this.sampleRate,
          }
        });
  
        this.mediaRecorder = new MediaRecorder(this.stream, {
          mimeType: 'audio/webm'
        });
  
        this.setupEventListeners();
        return true;
      } catch (error) {
        console.error('Failed to initialize recorder:', error);
        return false;
      }
    }
  
    private setupEventListeners(): void {
      if (!this.mediaRecorder) return;
  
      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data);
        }
      };
    }
  
    start(): void {
      this.audioChunks = [];
      this.mediaRecorder?.start();
    }
  
    stop(): Promise<Blob> {
      return new Promise((resolve) => {
        if (!this.mediaRecorder) {
          resolve(new Blob([]));
          return;
        }
  
        this.mediaRecorder.onstop = async () => {
          try {
            const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
            const wavBlob = await this.convertToWAV(audioBlob);
            resolve(wavBlob);
          } catch (error) {
            console.error('Error converting audio:', error);
            resolve(new Blob([]));
          } finally {
            this.cleanup();
          }
        };
  
        this.mediaRecorder.stop();
      });
    }
  
    cleanup(): void {
      this.stream?.getTracks().forEach(track => track.stop());
      this.audioChunks = [];
    }
  
    private async convertToWAV(audioBlob: Blob): Promise<Blob> {
      try {
        // Convert blob to array buffer
        const arrayBuffer = await audioBlob.arrayBuffer();
        const audioContext = new AudioContext({
          sampleRate: this.sampleRate,
        });
  
        // Decode audio data
        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
        const audioData = audioBuffer.getChannelData(0); // Get first channel
  
        // WAV header parameters
        const numChannels = 1;
        const bitDepth = 16;
        const bytesPerSample = bitDepth / 8;
        const blockAlign = numChannels * bytesPerSample;
        const byteRate = this.sampleRate * blockAlign;
        const dataSize = audioData.length * bytesPerSample;
        const bufferSize = 44 + dataSize;
  
        // Create buffer for the WAV file
        const buffer = new ArrayBuffer(bufferSize);
        const view = new DataView(buffer);
  
        // Write WAV header
        this.writeString(view, 0, 'RIFF');
        view.setUint32(4, 36 + dataSize, true);
        this.writeString(view, 8, 'WAVE');
        
        // fmt sub-chunk
        this.writeString(view, 12, 'fmt ');
        view.setUint32(16, 16, true);
        view.setUint16(20, 1, true);
        view.setUint16(22, numChannels, true);
        view.setUint32(24, this.sampleRate, true);
        view.setUint32(28, byteRate, true);
        view.setUint16(32, blockAlign, true);
        view.setUint16(34, bitDepth, true);
  
        // data sub-chunk
        this.writeString(view, 36, 'data');
        view.setUint32(40, dataSize, true);
  
        // Write audio data
        this.floatTo16BitPCM(view, 44, audioData);
  
        return new Blob([buffer], { type: 'audio/wav' });
      } catch (error) {
        console.error('Error in WAV conversion:', error);
        throw error;
      }
    }
  
    private writeString(view: DataView, offset: number, string: string): void {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    }
  
    private floatTo16BitPCM(view: DataView, offset: number, input: Float32Array): void {
      for (let i = 0; i < input.length; i++, offset += 2) {
        const s = Math.max(-1, Math.min(1, input[i]));
        view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
      }
    }
  }