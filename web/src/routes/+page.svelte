<script lang="ts">
    // Importing in Svelte automatically includes the directory
    import { QuarryEngine } from "$lib/logic/game.svelte";
    import { playedTrackIds, clearHistory } from "$lib/stores/game";
    import type { MusicTrack } from "$lib/core/interfaces.js";
    import { fade } from 'svelte/transition'

    // Blueprint
    interface PageProps {
        data : {
            tracks: MusicTrack[];
        }
    }

    let { data }: PageProps = $props();
    // Props is a rune that receive the Data in OBJECT FORM
    // { } is destructuring, meaning we only want the item labled "data"

    /** EXAMPLE
     * we want to send a button for send
     * we can send the label = "SEND" and the color,
     * props will receive it and we only want the send and color blue
     * let { label, color = 'blue'} = $props();
     * // blue is a fallback (HELPFUL)
     * and we can use it like this.
     * <button style="background: {color}">
            {label}
        </button> 
     * 
     */

   // FIX: Initialize with empty array to avoid the "local reference" error
    const game = new QuarryEngine([]); 

    // This effect runs immediately on mount and whenever data changes.
    // It is the "Source of Truth" for your engine.
    $effect(() => {
        // This makes the engine reactive to prop changes!
        game.tracks = data.tracks; 
        
        // Only set index if within bounds (safety check)
        game.currentIndex = $playedTrackIds.length;
    });
    // Constantly checking
</script>

<main class="p-8 font-sans bg-zinc-950 text-white min-h-screen">
    <h1 class="text-2xl font-bold mb-4">QUARRY DEBUG MODE</h1>

    <div class="mb-8 p-4 bg-zinc-900 rounded">
        <p>Tracks in Pack: {game.tracks.length}</p>
        <p>Played History (Store): {$playedTrackIds.length}</p>
        {#if game.currentIndex > 1}
            <div class="flex gap-4">
                <button 
                    onclick={ () => {
                        clearHistory();
                        game.reset();
                    }}
                    class="px-6 py-2 bg-white text-black font-bold rounded hover:bg-zinc-200"
                >
                    Reset
                </button>
            </div>
        {/if}
    </div>

    {#if game.tracks.length === 0}
        <div class="flex items-center justify-center h-64 text-zinc-500 animate-pulse">
            Loading Game Data...
        </div>
    
    {:else if game.currentIndex < game.tracks.length}
        {#if game.currentTrack}
            <div class="space-y-4 border-l-4 border-green-500 pl-6">
                <div class="h-20">
                    {#if game.isRevealed}
                        <h2 class="text-xl font-bold">{game.currentTrack.title}</h2>
                        <p class="text-zinc-400">{game.currentTrack.artist}</p>
                    {:else}
                        <div class="text-zinc-600 italic">[ Track Info Hidden ]</div>
                    {/if}
                </div>

               <div class="flex gap-4">
                    <button 
                        onclick={() => game.playClip(5)}
                        class="px-6 py-2 bg-white text-black font-bold rounded hover:bg-zinc-200"
                    >
                        {game.isPlaying ? '🔊 Playing...' : '▶️ Play 5s'}
                    </button>

                    {#if !game.isRevealed}
                        <button 
                            transition:fade={{ duration: 150 }}
                            onclick={() => game.reveal()}
                            class="px-6 py-2 bg-zinc-800 rounded hover:bg-zinc-700"
                        >
                            🔍 Reveal
                        </button>
                    {:else}
                        <button 
                            transition:fade={{ duration: 150 }}
                            onclick={() => game.next()}
                            class="px-6 py-2 bg-blue-600 rounded hover:bg-blue-500"
                        >
                            Next ⏭️
                        </button>
                    {/if}
                </div>
            </div>
        {:else}
            <p class="text-red-500">Error: Track data missing.</p>
        {/if}
    {:else}
        <div class="text-center py-12 bg-zinc-900/50 rounded-xl border border-zinc-800">
            <h2 class="text-3xl font-bold mb-2">Pack Completed! 🎉</h2>
            <p class="text-zinc-400 mb-6">You've guessed every song in this set.</p>
            <button 
                onclick={() => {
                    clearHistory();
                    game.reset();
                }}
                class="px-8 py-3 bg-white text-black font-bold rounded-full hover:scale-105 transition-transform"
            >
                Play Again
            </button>
        </div>
    {/if}
</main>