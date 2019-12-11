
from automation import CommandSequence, TaskManager

# The list of sites that we wish to crawl
NUM_BROWSERS = 3
sites = ['https://www.de.quora.com', 'https://www.paypal.com/de/home/', 'https://www.google.de/', 'https://www8.hp.com/de/de/home.html', 'https://www.microsoft.com/de-de/', 'https://www.myvideo.ge/', 'https://www.intel.de/content/www/de/de/homepage.html', 'https://www.mozilla.de/', 'https://www.nvidia.com/de-de/', 'https://wikipedia.de/', 'https://www.dell.com/de-de?c=de&l=de&s=gen&mp=dell.de/&redirect=1', 'https://www.msn.com/de-de', 'https://www.airbnb.de/', 'https://www.teamviewer.com/de/', 'https://discovery.de/', 'https://de.wordpress.com/', 'https://stackoverflow.com/', 'https://www.verizonmedia.com/de', 'https://www.amazon.de/', 'https://www.ebay.de/', 'https://twitter.com/', 'https://www.spiegel.de/', 'https://www.dropbox.com/de', 'https://www.bestbuy.com', 'https://www.adobe.com', 'https://www.spotify.com', 'https://de.indeed.com/', 'https://www.paypal.com/de/home/', 'https://www.dhl.de/en/privatkunden.html', 'https://www.salesforce.com/de/?rd=de', 'https://de.linkedin.com/', 'https://www.apple.com/de/', 'https://www.kleinanzeigen.de/', 'https://www.bahn.de/p/view/index.shtml', 'https://de-de.facebook.com/', 'https://www.pinterest.de/', 'https://www.samsung.com/de/', 'https://de.reddit.com/', 'https://www.shopify.de/', 'https://www.booking.com/index.de.html?aid=202008']

# Loads the default manager params
# and NUM_BROWSERS copies of the default browser params
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in range(NUM_BROWSERS):
    # Record HTTP Requests and Responses
    browser_params[i]['http_instrument'] = True
    # Record cookie changes
    browser_params[i]['cookie_instrument'] = True
    # Record Navigations
    browser_params[i]['navigation_instrument'] = True
    # Record JS Web API calls
    browser_params[i]['js_instrument'] = True
    # Enable flash for all three browsers
    browser_params[i]['disable_flash'] = True
browser_params[0]['headless'] = True  # Launch only browser 0 headless

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/Desktop/'
manager_params['log_directory'] = '~/Desktop/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites
for site in sites:

    # Parallelize sites over all number of browsers set above.
    # (To have all browsers go to the same sites, add `index='**'`)
    command_sequence = CommandSequence.CommandSequence(site, reset=True)

    # Start by visiting the page
    command_sequence.get(sleep=3, timeout=120)
    
   
    #command_sequence.dump_page_source('dump', timeout=120)
    command_sequence.save_screenshot('screenshot', timeout=120)
    # Run commands across the three browsers (simple parallelization)
    manager.execute_command_sequence(command_sequence)

# Shuts down the browsers and waits for the data to finish logging
manager.close()
