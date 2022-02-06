#### These instructions do _only_ improve the performance of the script significantally if you own over 100 steam packages.

1. Execute `activate_packages` for the 1st time
2. Copy script to Clipboard
```js
var elements = document.querySelectorAll(
    "div[class='free_license_remove_link'] > a"
);
var games = "";
for (let i = 0; i < elements.length; i++) {
    var game = elements[i].href;
    game = game.match(/([1-9])\w+/g)[0];
    games += game + ",";
}
console.log(games);
```
3. Open your [licenses and product key activations](https://store.steampowered.com/account/licenses/) page
4. Open developer tools in your browser, [read more here](https://webmasters.stackexchange.com/questions/8525/how-do-i-open-the-javascript-console-in-different-browsers/77337#77337)
5. Paste script (which is in your clipboard) into the console
6. Copy the console output, which should look something like this:
```
430369,370157,367877,452385,122355,662406,
```
8. Open the `activated_packages.txt` file in a text editor
9. Delete the existing file content
10. Paste console output (which is in your clipboard) into the file
11. Save the file
12. Execute `activate_packages` to activate packages
