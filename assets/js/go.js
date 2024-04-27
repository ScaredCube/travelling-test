const prefix = "t_preference_";
const getSetting = key => localStorage.getItem(prefix + key);

const preferredTag = getSetting("tag");
const travellingTimeout = getSetting("timeout") || 1500;

let apiUrl = "https://api.travellings.cn/random";
if (preferredTag) apiUrl += "?tag=" + preferredTag;

let go = async () => {
    let res = await fetch(apiUrl);
    res = await res.json();
    if (!res.success) {
        alert("�ǳ���Ǹ����˷��������������⣬���Ժ�����~")
        return;
    }
    location.href = res.data[0].url;
}

setTimeout(go, travellingTimeout);
