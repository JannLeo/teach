// this part is copied from kms5main.js for use on pages where kms5main.js is not loaded (ie secure embed)
if(!window.kms_playerV7Handler){
    window.kms_playerV7Handler = {
        loaded: function(entryId, isRaptEntry) {
            isRaptEntry = isRaptEntry || false;
            var event = document.createEvent("Event");
            event.entryId = entryId;
            if (isRaptEntry) {
                event.initEvent("kms_raptPlayerReady", true, true);
            }
            else {
                event.initEvent("kms_playerReady", true, true);
            }
            document.body.dispatchEvent(event);
        }
    };
}
