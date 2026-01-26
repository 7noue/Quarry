// import { markAsPlayed } from '$lib/stores/game';
// import type { MusicTrack } from '$lib/core/interfaces';

export class QuarryEngine {
    // RUNES: Reactive state for Svelte 5
    tracks = $state<MusicTrack[]>([]);
    currentIndex = $state(0);
    isPlaying = $state(false)
    isRevealead = $state(false)
    audioElement: HTMLAudioElement | null = null;




}