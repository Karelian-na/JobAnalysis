var searchParam = new window.URLSearchParams(window.location.search)
seed = searchParam.get("seed")
timestamp = searchParam.get("timestamp")

var myt = new window.ABC
newCookie = myt.z(seed, parseInt(timestamp) + 60 * (480 + (new Date).getTimezoneOffset()) * 1e3)
$.ajax({
    method: "GET",
    url: "/setBossNewCookie",
    data: `value=${newCookie}`,
    success: (result) => {
        console.log(result)
    },
    error: (_xhr, _status, _error) => {
        window.alert(_error);
    },
});