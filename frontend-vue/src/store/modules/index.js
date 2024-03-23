const requireModule = require.context('.', false, /\.store\.js$/);
const modules = {}

requireModule.keys().forEach(filename => {
    // create the module name from the filename
    // remove the store.js extension and capitalize the first letter
    const moduleName = filename
                        .replace(/(\.\/|\.store\.js)/g, '')
                        .replace(/^\w/, firstLetter => firstLetter.toUpperCase())

    modules[moduleName] = requireModule(filename).default || requireModule(filename)
});

export default modules
