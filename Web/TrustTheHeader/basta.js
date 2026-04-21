fetch("http://178.128.110.55:6823/admin", {
      headers: { "X-admin": "true"}
}).then(r => r.text()).then(console.log)

// can also do this:
// curl -i http://178.128.110.55:6823/admin   -H 'X-Admin: true'