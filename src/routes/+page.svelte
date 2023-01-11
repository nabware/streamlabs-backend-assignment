{#if isLoading}
    <div style="text-align: center; margin-top: 187px;">
        <div class="loader"></div>
        <div style="color: hsl(0,0%,50%); margin-top: 20px;">Loading ...</div>
    </div>
{:else}
    {#if sessionId}
        <div style="text-align: center;">
            <h2>250</h2>
            <p style="color: hsl(0,0%,50%);">subscribers</p>
            <a href="" class="link-button" on:click={signOut}><i class="fa-solid fa-right-from-bracket link-button-icon" />Sign out</a>
        </div>
    {:else}
        <div style="text-align: center; margin-top: 227px;">
            <a href="" on:click={redirectToLogin}>
                <img src="./btn_google_signin_dark_normal_web.png" alt="Sign in with Google" />
            </a>
        </div>
    {/if}
{/if}


<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';

    let isLoading: boolean = false;
    let sessionId: string | null;

    onMount(main);

    async function main() {
        isLoading = true;

        const state = $page.url.searchParams.get('state');
        const code = $page.url.searchParams.get('code');
        goto("/", { replaceState: true });

        sessionId = sessionStorage.getItem('sessionId');
        if (sessionId) {
            isLoading = false;
            return;
        }

        if (!state || !code) {
            isLoading = false;
            return;
        }

        const codeVerifier = sessionStorage.getItem(`codeVerifier-${state}`);
        sessionStorage.removeItem(`codeVerifier-${state}`);

        try {
            if (codeVerifier === null) {
                throw new Error('Unexpected code');
            }
            sessionId = '123';
            sessionStorage.setItem('sessionId', sessionId);
        } catch (error) {
            alert(error);
        }

        isLoading = false;
    }

    async function redirectToLogin() {
        const state = await generateNonce();
        const codeVerifier = await generateNonce();
        sessionStorage.setItem(`codeVerifier-${state}`, codeVerifier);
        const codeChallenge = base64UrlEncode(await sha256(codeVerifier));
        goto(`${import.meta.env.VITE_COGNITO_URL}/oauth2/authorize?response_type=code&client_id=${import.meta.env.VITE_COGNITO_CLIENT_ID}&state=${state}&code_challenge_method=S256&code_challenge=${codeChallenge}&redirect_uri=${import.meta.env.VITE_COGNITO_REDIRECT_URI}&identity_provider=Google`);
    }

    async function generateNonce () {
        const hash = await sha256(crypto.getRandomValues(new Uint32Array(4)).toString());
        // https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/digest
        const hashArray = Array.from(new Uint8Array(hash));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    }

    async function sha256(string: string) {
        return await crypto.subtle.digest('SHA-256', new TextEncoder().encode(string));
    }

    function base64UrlEncode(arrayBuffer: ArrayBuffer) {
        return btoa(String.fromCharCode.apply(null, Array.from<number>(new Uint8Array(arrayBuffer))))
            .replace(/\+/g, '-')
            .replace(/\//g, '_')
            .replace(/=+$/, '');
    }

    function signOut() {
        sessionStorage.clear();
        goto(`${import.meta.env.VITE_COGNITO_URL}/logout?client_id=${import.meta.env.VITE_COGNITO_CLIENT_ID}&logout_uri=${import.meta.env.VITE_COGNITO_REDIRECT_URI}`);
    }

</script>