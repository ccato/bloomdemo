<script>
  import { Check, AlertCircle, Loader2 } from "lucide-svelte";

  let username = $state("");
  let status = $state({ exists: null, suggestions: [] });
  let loading = $state(false);
  let isFocused = $state(false);

  let timeout;

  $effect(() => {
    clearTimeout(timeout);

    if (username.length < 3) {
      status = { exists: null, suggestions: [] };
      loading = false;
      return;
    }

    timeout = setTimeout(async () => {
      loading = true;

      try {
        const res = await fetch("/api/check", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username })
        });

        const data = await res.json();
        status = {
          exists: data.exists,
          suggestions: data.suggestions || []
        };
      } catch (err) {
        console.error("API Error", err);
      } finally {
        loading = false;
      }
    }, 400);
  });
</script>

<div class="picker-container">
  <div class="input-group {isFocused ? 'focused' : ''} {status.exists === true ? 'error' : ''}">

    <label class={(isFocused || username) ? 'shrink' : ''}>
      Pick a username
    </label>

    <div class="input-flex">
      <input
        type="text"
        bind:value={username}
        on:focus={() => isFocused = true}
        on:blur={() => isFocused = false}
        spellcheck="false"
      />

      <div class="icon-feedback">
        {#if loading}
          <Loader2 class="animate-spin" size={18} />
        {:else if status.exists === false}
          <Check size={18} color="#0b8043" stroke-width={3} />
        {:else if status.exists === true}
          <AlertCircle size={18} color="#d93025" />
        {/if}
      </div>
    </div>
  </div>

  {#if status.exists === true}
    <div class="error-msg">
      That username is taken. Try another.

      <div class="username-suggestions">
        Available:
        {#each status.suggestions as s}
          <button on:click={() => username = s}>{s}</button>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  @import "../App.css";
</style>