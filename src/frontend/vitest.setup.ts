import '@testing-library/jest-dom';

// Polyfill browser APIs not present in jsdom to avoid runtime errors in effects
// scrollTo is not implemented on HTMLElement in jsdom
if (!('scrollTo' in HTMLElement.prototype)) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (HTMLElement.prototype as any).scrollTo = () => { };
}

// requestAnimationFrame/cancelAnimationFrame polyfills for jsdom/node
if (typeof globalThis.requestAnimationFrame !== 'function') {
    globalThis.requestAnimationFrame = (cb: FrameRequestCallback): number => {
        return setTimeout(() => cb(performance.now()), 0) as unknown as number;
    };
}
if (typeof globalThis.cancelAnimationFrame !== 'function') {
    globalThis.cancelAnimationFrame = (id: number) => {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        clearTimeout(id as any);
    };
}
