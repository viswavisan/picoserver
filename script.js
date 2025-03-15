function togglePin(pin, state) {
    if (pin=='LED'){
        fetch('/execute', {method: 'POST',body: JSON.stringify({ cmd: state ? 'led.on()' : 'led.off()' })});  
        }
    }



document.addEventListener('DOMContentLoaded', () => {
    function create_switches(){
    const container = document.getElementById('left-switches');
    for (let i = 1; i <= 20; i++) {
        container.innerHTML += `
            <label class="toggle-switch" style="align-self: anchor-center;">
                <input type="checkbox" onchange="togglePin('pin${i}', this.checked)">${i}
            </label>`;}

    const container2 = document.getElementById('right-switches');
    for (let i = 40; i >= 21; i--) {
        container2.innerHTML += `
            <label class="toggle-switch" style="align-self: anchor-center;">
                <input type="checkbox" onchange="togglePin('pin${i}', this.checked)">${i}
            </label>`;}
    const container3 = document.getElementById('imagerow');
    container3.innerHTML = `
        <label class="toggle-switch" style="align-self: anchor-center;">
            <input type="checkbox" onchange="togglePin('LED', this.checked)">BOARD-LED
        </label>`+container3.innerHTML}

create_switches()




async function connectWiFi() {
    const ssid = document.getElementById('wifi_list').value;
    const password = prompt("Enter Password:");
    const wstate = document.getElementById('wstate')
    wstate.textContent='connecting...'
    if (ssid && password) {
        console.log(ssid)
        console.log(password)
        fetch('/execute', {method: 'POST',body: JSON.stringify({ cmd: `return_value["data"]=connection.connect_wifi('${ssid}','${password}')`})})
        .then(response => response.json())
        .then(data=>{wstate.textContent=data['data']['message']})
    } else {
        alert('SSID and Password are required');
    }
}
function scan_wifi() {
    console.log('scanning')
        fetch('/execute', {method: 'POST',body: JSON.stringify({ cmd: 'return_value["data"]=[network_info[0].decode() for network_info in connection.wlan.scan()]' })}).then(response => response.json())
        .then (data=>{
            const wifiSelect = document.getElementById('wifi_list');
            data['data'].forEach(ssid => wifiSelect.add(new Option(ssid, ssid)))})
    }

    async function connectWiFi1() {

        const wstate1 = document.getElementById('wstate')
        fetch('/execute', {method: 'POST',body: JSON.stringify({ cmd: `return_value["data"]=connection.check_status()`})})
        .then(response => response.json())
        .then(data=>{wstate1.textContent=data['data']['message']})
        console.log('ok')
    }
    connectWiFi1()


    document.getElementById('connect_wifi').addEventListener('click', connectWiFi);
    document.getElementById('scan').addEventListener('click', scan_wifi);
    scan_wifi()

    document.getElementById('pico_image').src="https://logicaprogrammabile.it/wp-content/uploads/2021/02/pipo_pinout.jpg"
});