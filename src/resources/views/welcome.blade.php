<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>CampainhaInt</title>

        <!-- Script -->
        {{-- <script src="{{ resource('js/app.js') }}"></script> --}}

        <!-- Styles -->
        {{-- <link rel="stylesheet" href="{{ resource('css/app.css') }}"> --}}
        {{-- O vite carrega e constroi as dependencias --}}
        @vite(['resources/css/app.css', 'resources/js/app.js'])
    </head>
    <noscript>
        <div style="display: absolute; top: 45%; left: 45%; z-index: 10; border: 1px solid #000000; padding: 10px;" class="semjs">
            <p style="color: #921616;">Essa aplicação necessita de Javascript para funcionar!<br> Ative o Javascript!</p>
        </div>
    </noscript>
    <body class="antialiased">
        <div id="app">

        </div>
    </body>
</html>
