export function translateString(string) {
    if (typeof window !== 'undefined' && window.TRANSLATION && typeof window.TRANSLATION[string] === 'string') {
        return window.TRANSLATION[string];
    }
    return string;
}

export function translateSecondsLabel(seconds, unitKey = 'seconds') {
    const unit = translateString(unitKey);
    return `${seconds} ${unit}`;
}
