Title: default | wavesurfer.js

URL Source: https://wavesurfer.xyz/docs/classes/wavesurfer.default

Markdown Content:
Constructors
------------

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### constructor[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#constructor)

*   new default(options): [default](https://wavesurfer.xyz/docs/classes/wavesurfer.default.html)[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#constructor.new_default)
*   #### Returns [default](https://wavesurfer.xyz/docs/classes/wavesurfer.default.html)

Properties
----------

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Protected`abort Controller[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#abortController)

abort Controller:null | AbortController = null

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Private`decoded Data[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#decodedData)

decoded Data:null | AudioBuffer = null

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Protected`media[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#media)

media:HTMLMediaElement

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Protected`media Subscriptions[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#mediaSubscriptions)

media Subscriptions:(() =>void)[] = []

#### Type declaration

*       *   (): void
    *   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### options[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#options)

options:[WaveSurferOptions](https://wavesurfer.xyz/docs/types/wavesurfer.WaveSurferOptions.html)&{ 

autoCenter: boolean; 

autoScroll: boolean; 

cursorWidth: number; 

dragToSeek: boolean; 

fillParent: boolean; 

interact: boolean; 

minPxPerSec: number; 

progressColor: string; 

sampleRate: number; 

waveColor: string; 

}

#### Type declaration

*   ##### auto Center: boolean

*   ##### auto Scroll: boolean

*   ##### cursor Width: number

*   ##### drag To Seek: boolean

*   ##### fill Parent: boolean

*   ##### interact: boolean

*   ##### min Px Per Sec: number

*   ##### progress Color: string

*   ##### sample Rate: number

*   ##### wave Color: string

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Private`plugins[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#plugins)

plugins:GenericPlugin[] = []

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Private`renderer[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#renderer)

renderer:Renderer

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Private`stop At Position[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#stopAtPosition)

stop At Position:null | number = null

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Protected`subscriptions[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#subscriptions)

subscriptions:(() =>void)[] = []

#### Type declaration

*       *   (): void
    *   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Private`timer[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#timer)

timer:Timer

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Static``Readonly`Base Plugin[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#BasePlugin)

Base Plugin:typeof BasePlugin = BasePlugin

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Static``Readonly`dom[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#dom)

dom:__module = dom

Methods
-------

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### destroy[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#destroy)

*   destroy(): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#destroy.destroy-1)
*   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Protected`emit[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#emit)

*   emit<EventName>(eventName, ...args): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#emit.emit-1)
*   #### Type Parameters

    *   #### EventName extends keyof [WaveSurferEvents](https://wavesurfer.xyz/docs/types/wavesurfer.WaveSurferEvents.html)

#### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### empty[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#empty)

*   empty(): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#empty.empty-1)
*   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### export Image[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#exportImage)

*   export Image(format, quality, type): Promise<string[]>[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#exportImage.exportImage-1)
*   
#### Parameters

    *   ##### format: string

    *   ##### quality: number

    *   ##### type: "dataURL"

#### Returns Promise<string[]>

A promise that resolves with an array of data-URLs or blobs, one for each canvas element.

*   export Image(format, quality, type): Promise<Blob[]>[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#exportImage.exportImage-2)
*   
#### Parameters

    *   ##### format: string

    *   ##### quality: number

    *   ##### type: "blob"

#### Returns Promise<Blob[]>

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### export Peaks[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#exportPeaks)

*   export Peaks(__namedParameters?): number[][][](https://wavesurfer.xyz/docs/classes/wavesurfer.default#exportPeaks.exportPeaks-1)
*   
#### Parameters

    *   ##### __namedParameters: { 

channels: undefined | number; 

maxLength: undefined | number; 

precision: undefined | number; 

} = {}

        *   ##### channels: undefined | number

        *   ##### max Length: undefined | number

        *   ##### precision: undefined | number

#### Returns number[][]

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### get Active Plugins[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getActivePlugins)

*   get Active Plugins(): GenericPlugin[][](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getActivePlugins.getActivePlugins-1)
*   #### Returns GenericPlugin[]

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### get Current Time[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getCurrentTime)

*   get Current Time(): number[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getCurrentTime.getCurrentTime-1)
*   #### Returns number

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### get Decoded Data[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getDecodedData)

*   get Decoded Data(): null | AudioBuffer[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getDecodedData.getDecodedData-1)
*   #### Returns null | AudioBuffer

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### get Duration[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getDuration)

*   get Duration(): number[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getDuration.getDuration-1)
*   #### Returns number

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### get Media Element[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getMediaElement)

*   get Media Element(): HTMLMediaElement[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getMediaElement.getMediaElement-1)
*   #### Returns HTMLMediaElement

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### get Muted[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getMuted)

*   get Muted(): boolean[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getMuted.getMuted-1)
*   #### Returns boolean

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### get Playback Rate[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getPlaybackRate)

*   get Playback Rate(): number[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getPlaybackRate.getPlaybackRate-1)
*   #### Returns number

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### get Scroll[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getScroll)

*   get Scroll(): number[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getScroll.getScroll-1)
*   #### Returns number

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Protected`get Src[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getSrc)

*   get Src(): string[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getSrc.getSrc-1)
*   #### Returns string

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### get Volume[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getVolume)

*   get Volume(): number[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getVolume.getVolume-1)
*   #### Returns number

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### get Width[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getWidth)

*   get Width(): number[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getWidth.getWidth-1)
*   #### Returns number

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### get Wrapper[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getWrapper)

*   get Wrapper(): HTMLElement[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#getWrapper.getWrapper-1)
*   #### Returns HTMLElement

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Private`init Player Events[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#initPlayerEvents)

*   init Player Events(): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#initPlayerEvents.initPlayerEvents-1)
*   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Private`init Plugins[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#initPlugins)

*   init Plugins(): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#initPlugins.initPlugins-1)
*   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Private`init Renderer Events[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#initRendererEvents)

*   init Renderer Events(): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#initRendererEvents.initRendererEvents-1)
*   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Private`init Timer Events[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#initTimerEvents)

*   init Timer Events(): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#initTimerEvents.initTimerEvents-1)
*   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### is Playing[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#isPlaying)

*   is Playing(): boolean[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#isPlaying.isPlaying-1)
*   #### Returns boolean

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### is Seeking[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#isSeeking)

*   is Seeking(): boolean[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#isSeeking.isSeeking-1)
*   #### Returns boolean

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### load[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#load)

*   load(url, channelData?, duration?): Promise<void>[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#load.load-1)
*   
#### Parameters

    *   ##### url: string

    *   ##### `Optional`channelData: (Float32Array | number[])[]

    *   ##### `Optional`duration: number

#### Returns Promise<void>

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Private`load Audio[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#loadAudio)

*   load Audio(url, blob?, channelData?, duration?): Promise<void>[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#loadAudio.loadAudio-1)
*   
#### Parameters

    *   ##### url: string

    *   ##### `Optional`blob: Blob

    *   ##### `Optional`channelData: (Float32Array | number[])[]

    *   ##### `Optional`duration: number

#### Returns Promise<void>

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### load Blob[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#loadBlob)

*   load Blob(blob, channelData?, duration?): Promise<void>[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#loadBlob.loadBlob-1)
*   
#### Parameters

    *   ##### blob: Blob

    *   ##### `Optional`channelData: (Float32Array | number[])[]

    *   ##### `Optional`duration: number

#### Returns Promise<void>

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### on[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#on)

*   on<EventName>(event, listener, options?): (() =>void)[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#on.on-1)
*   #### Type Parameters

    *   #### EventName extends keyof [WaveSurferEvents](https://wavesurfer.xyz/docs/types/wavesurfer.WaveSurferEvents.html)

#### Parameters

    *   ##### event: EventName

    *   ##### listener: EventListener<[WaveSurferEvents](https://wavesurfer.xyz/docs/types/wavesurfer.WaveSurferEvents.html), EventName>

    *   ##### `Optional`options: { 

once?: boolean; 

}

        *   ##### `Optional`once?: boolean

#### Returns (() =>void)

    *           *   (): void
        *   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Protected`on Media Event[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#onMediaEvent)

*   on Media Event<K>(event, callback, options?): (() =>void)[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#onMediaEvent.onMediaEvent-1)
*   #### Type Parameters

    *   #### K extends keyof HTMLElementEventMap

#### Parameters

    *   ##### event: K

    *   ##### callback: ((ev) =>void)

        *               *   (ev): void
            *   
#### Parameters

                *   ##### ev: HTMLElementEventMap[K]

#### Returns void

    *   ##### `Optional`options: boolean | AddEventListenerOptions

#### Returns (() =>void)

    *           *   (): void
        *   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### once[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#once)

*   once<EventName>(event, listener): (() =>void)[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#once.once-1)
*   #### Type Parameters

    *   #### EventName extends keyof [WaveSurferEvents](https://wavesurfer.xyz/docs/types/wavesurfer.WaveSurferEvents.html)

#### Parameters

    *   ##### event: EventName

    *   ##### listener: EventListener<[WaveSurferEvents](https://wavesurfer.xyz/docs/types/wavesurfer.WaveSurferEvents.html), EventName>

#### Returns (() =>void)

    *           *   (): void
        *   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### pause[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#pause)

*   pause(): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#pause.pause-1)
*   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### play[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#play)

*   play(start?, end?): Promise<void>[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#play.play-1)
*   
#### Parameters

    *   ##### `Optional`start: number

    *   ##### `Optional`end: number

#### Returns Promise<void>

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### play Pause[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#playPause)

*   play Pause(): Promise<void>[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#playPause.playPause-1)
*   #### Returns Promise<void>

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### register Plugin[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#registerPlugin)

*   register Plugin<T>(plugin): T[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#registerPlugin.registerPlugin-1)
*   #### Type Parameters

    *   #### T extends GenericPlugin

#### Parameters

    *   ##### plugin: T

#### Returns T

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### seek To[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#seekTo)

*   seek To(progress): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#seekTo.seekTo-1)
*   
#### Parameters

    *   ##### progress: number

#### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### set Media Element[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setMediaElement)

*   set Media Element(element): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setMediaElement.setMediaElement-1)
*   
#### Parameters

    *   ##### element: HTMLMediaElement

#### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### set Muted[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setMuted)

*   set Muted(muted): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setMuted.setMuted-1)
*   
#### Parameters

    *   ##### muted: boolean

#### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### set Options[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setOptions)

*   set Options(options): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setOptions.setOptions-1)
*   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### set Playback Rate[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setPlaybackRate)

*   set Playback Rate(rate, preservePitch?): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setPlaybackRate.setPlaybackRate-1)
*   
#### Parameters

    *   ##### rate: number

    *   ##### `Optional`preservePitch: boolean

#### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### set Scroll[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setScroll)

*   set Scroll(pixels): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setScroll.setScroll-1)
*   
#### Parameters

    *   ##### pixels: number

#### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### set Scroll Time[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setScrollTime)

*   set Scroll Time(time): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setScrollTime.setScrollTime-1)
*   
#### Parameters

    *   ##### time: number

#### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### set Sink Id[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setSinkId)

*   set Sink Id(sinkId): Promise<void>[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setSinkId.setSinkId-1)
*   
#### Parameters

    *   ##### sinkId: string

#### Returns Promise<void>

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Protected`set Src[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setSrc)

*   set Src(url, blob?): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setSrc.setSrc-1)
*   
#### Parameters

    *   ##### url: string

    *   ##### `Optional`blob: Blob

#### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### set Time[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setTime)

*   set Time(time): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setTime.setTime-1)
*   
#### Parameters

    *   ##### time: number

#### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### set Volume[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setVolume)

*   set Volume(volume): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#setVolume.setVolume-1)
*   
#### Parameters

    *   ##### volume: number

#### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### skip[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#skip)

*   skip(seconds): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#skip.skip-1)
*   
#### Parameters

    *   ##### seconds: number

#### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### stop[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#stop)

*   stop(): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#stop.stop-1)
*   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### toggle Interaction[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#toggleInteraction)

*   toggle Interaction(isInteractive): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#toggleInteraction.toggleInteraction-1)
*   
#### Parameters

    *   ##### isInteractive: boolean

#### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### un[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#un)

*   un<EventName>(event, listener): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#un.un-1)
*   #### Type Parameters

    *   #### EventName extends keyof [WaveSurferEvents](https://wavesurfer.xyz/docs/types/wavesurfer.WaveSurferEvents.html)

#### Parameters

    *   ##### event: EventName

    *   ##### listener: EventListener<[WaveSurferEvents](https://wavesurfer.xyz/docs/types/wavesurfer.WaveSurferEvents.html), EventName>

#### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### un All[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#unAll)

*   un All(): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#unAll.unAll-1)
*   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Private`unsubscribe Player Events[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#unsubscribePlayerEvents)

*   unsubscribe Player Events(): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#unsubscribePlayerEvents.unsubscribePlayerEvents-1)
*   #### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Private`update Progress[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#updateProgress)

*   update Progress(currentTime?): number[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#updateProgress.updateProgress-1)
*   
#### Parameters

    *   ##### currentTime: number = ...

#### Returns number

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### zoom[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#zoom)

*   zoom(minPxPerSec): void[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#zoom.zoom-1)
*   
#### Parameters

    *   ##### minPxPerSec: number

#### Returns void

[](https://wavesurfer.xyz/docs/classes/wavesurfer.default)
### `Static`create[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#create)

*   create(options): [default](https://wavesurfer.xyz/docs/classes/wavesurfer.default.html)[](https://wavesurfer.xyz/docs/classes/wavesurfer.default#create.create-1)
*   #### Returns [default](https://wavesurfer.xyz/docs/classes/wavesurfer.default.html)

---

Title: WaveSurferOptions | wavesurfer.js

URL Source: https://wavesurfer.xyz/docs/types/wavesurfer.WaveSurferOptions

Markdown Content:
Wave Surfer Options:{ 

audioRate?: number; 

autoCenter?: boolean; 

autoScroll?: boolean; 

autoplay?: boolean; 

backend?: "WebAudio" | "MediaElement"; 

barAlign?: "top" | "bottom"; 

barGap?: number; 

barHeight?: number; 

barRadius?: number; 

barWidth?: number; 

blobMimeType?: string; 

container: HTMLElement | string; 

cspNonce?: string; 

cursorColor?: string; 

cursorWidth?: number; 

dragToSeek?: boolean | { 

debounceTime: number; 

}; 

duration?: number; 

fetchParams?: RequestInit; 

fillParent?: boolean; 

height?: number | "auto"; 

hideScrollbar?: boolean; 

interact?: boolean; 

media?: HTMLMediaElement; 

mediaControls?: boolean; 

minPxPerSec?: number; 

normalize?: boolean; 

peaks?: (Float32Array | number[])[]; 

plugins?: GenericPlugin[]; 

progressColor?: string | string[] | CanvasGradient; 

renderFunction?: ((peaks, ctx) =>void); 

sampleRate?: number; 

splitChannels?: (Partial<[WaveSurferOptions](https://wavesurfer.xyz/docs/types/wavesurfer.WaveSurferOptions.html)>&{ 

overlay?: boolean; 

})[]; 

url?: string; 

waveColor?: string | string[] | CanvasGradient; 

width?: number | string; 

}

#### Type declaration

*   ##### `Optional`audio Rate?: number

*   ##### `Optional`auto Center?: boolean

*   ##### `Optional`auto Scroll?: boolean

*   ##### `Optional`autoplay?: boolean

*   ##### `Optional`backend?: "WebAudio" | "MediaElement"

*   ##### `Optional`bar Align?: "top" | "bottom"

*   ##### `Optional`bar Gap?: number

*   ##### `Optional`bar Height?: number

*   ##### `Optional`bar Radius?: number

*   ##### `Optional`bar Width?: number

*   ##### `Optional`blob Mime Type?: string

*   ##### container: HTMLElement | string

*   ##### `Optional`csp Nonce?: string

*   ##### `Optional`cursor Color?: string

*   ##### `Optional`cursor Width?: number

*   ##### `Optional`drag To Seek?: boolean | { 

debounceTime: number; 

}

*   ##### `Optional`duration?: number

*   ##### `Optional`fetch Params?: RequestInit

*   ##### `Optional`fill Parent?: boolean

*   ##### `Optional`height?: number | "auto"

*   ##### `Optional`hide Scrollbar?: boolean

*   ##### `Optional`interact?: boolean

*   ##### `Optional`media?: HTMLMediaElement

*   ##### `Optional`media Controls?: boolean

*   ##### `Optional`min Px Per Sec?: number

*   ##### `Optional`normalize?: boolean

*   ##### `Optional`peaks?: (Float32Array | number[])[]

*   ##### `Optional`plugins?: GenericPlugin[]

*   ##### `Optional`progress Color?: string | string[] | CanvasGradient

*   ##### `Optional`render Function?: ((peaks, ctx) =>void)

    *           *   (peaks, ctx): void
        *   
#### Parameters

            *   ##### peaks: (Float32Array | number[])[]

            *   ##### ctx: CanvasRenderingContext2D

#### Returns void

*   ##### `Optional`sample Rate?: number

*   ##### `Optional`split Channels?: (Partial<[WaveSurferOptions](https://wavesurfer.xyz/docs/types/wavesurfer.WaveSurferOptions.html)>&{ 

overlay?: boolean; 

})[]

*   ##### `Optional`url?: string

*   ##### `Optional`wave Color?: string | string[] | CanvasGradient

*   ##### `Optional`width?: number | string

---

Title: WaveSurferEvents | wavesurfer.js

URL Source: https://wavesurfer.xyz/docs/types/wavesurfer.WaveSurferEvents

Markdown Content:
Wave Surfer Events:{ 

audioprocess: [currentTime: number]; 

click: [relativeX: number, relativeY: number]; 

dblclick: [relativeX: number, relativeY: number]; 

decode: [duration: number]; 

destroy: []; 

drag: [relativeX: number]; 

dragend: [relativeX: number]; 

dragstart: [relativeX: number]; 

error: [error: Error]; 

finish: []; 

init: []; 

interaction: [newTime: number]; 

load: [url: string]; 

loading: [percent: number]; 

pause: []; 

play: []; 

ready: [duration: number]; 

redraw: []; 

redrawcomplete: []; 

scroll: [visibleStartTime: number, visibleEndTime: number, scrollLeft: number, scrollRight: number]; 

seeking: [currentTime: number]; 

timeupdate: [currentTime: number]; 

zoom: [minPxPerSec: number]; 

}

#### Type declaration

*   ##### audioprocess: [currentTime: number]

*   ##### click: [relativeX: number, relativeY: number]

*   ##### dblclick: [relativeX: number, relativeY: number]

*   ##### decode: [duration: number]

*   ##### destroy: []

*   ##### drag: [relativeX: number]

*   ##### dragend: [relativeX: number]

*   ##### dragstart: [relativeX: number]

*   ##### error: [error: Error]

*   ##### finish: []

*   ##### init: []

*   ##### interaction: [newTime: number]

*   ##### load: [url: string]

*   ##### loading: [percent: number]

*   ##### pause: []

*   ##### play: []

*   ##### ready: [duration: number]

*   ##### redraw: []

*   ##### redrawcomplete: []

*   ##### scroll: [visibleStartTime: number, visibleEndTime: number, scrollLeft: number, scrollRight: number]

*   ##### seeking: [currentTime: number]

*   ##### timeupdate: [currentTime: number]

*   ##### zoom: [minPxPerSec: number]