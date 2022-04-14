""" pyOdourCollect: A tool that obtains odour observations made by citizens at odourcollect.eu Citizen Obsevatory.
"""
import argparse
import datetime
import ochelpers
import occore
import ocmodels


def main():
    argparser = argparse.ArgumentParser(
        prog='OdourCollect',
        description='pyOdourCollect: A tool that obtains odour observations made by citizens at odourcollect.eu Citizen Obsevatory.',
        epilog='Run this program with --odourlist parameter for a full list of odour categories and types.'
    )
    filteropts = argparser.add_argument_group('Observation filter options')
    filteropts.add_argument("--startdate", "-s", type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
                            help="Earliest date (yyyy-mm-dd).")
    filteropts.add_argument("--enddate", "-e", type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
                            help="Latest date (yyyy-mm-dd).")
    filteropts.add_argument("--category", "-c", type=int,
                            help="Category of odours (known as 'type' in OdourCollect) From 1 to 9. 0 means all.")
    filteropts.add_argument("--odourtype", "-t", type=int, default=0,
                            help="Type of odour (known as 'subtype' in OdourCollect). From 1 to 89. 0 means all.")
    filteropts.add_argument("--hedonic", default='all', const='all', nargs='?',
                            choices=['pleasant', 'unpleasant', 'neutral', 'all'],
                            help="Hedonic tones. \"unpleasant\" (from -1 to -4), \"pleasant\" (from +1 to +4), \"neutral\" (tone zero only) or \"all\" (get everything, default")
    filteropts.add_argument("--minintensity", type=int,
                            help="Minimum intensity of odour, from 0 to 6.")
    filteropts.add_argument("--maxintensity", type=int,
                            help="Maximum intensity of odour, from 0 to 6.")
    analysisopts = argparser.add_argument_group('Analysis options')
    analysisopts.add_argument("--gps", type=float, nargs=2, metavar=('lat', 'long'),
                              help="If specified, observations will include the distance in Km. from the specified GPS coordinates.\n"
                                   "Useful to analize data against a suspicious point of odour emission in a specific area of interest.\n"
                                   "Takes two arguments in the form of decimal numbers for lat/long gps coordenates i.e.:\n"
                                   "--gps 41.409032 2.222619")
    outputopts = argparser.add_argument_group('Output options')
    outputopts.add_argument("--output", type=str, default='odourcollect.csv', metavar='path to output file',
                            help="Dump the results in xlsx/csv format to the specified file\n"
                                 "If not specified, defaults to \"odourcollect.csv\". File format is autodetected based on extension.")
    helpopts = argparser.add_argument_group('List of odour categories and types')
    helpopts.add_argument("--odourlist", action='store_true',
                          help="Prints the full list of odour categories and types used in OdourCollect.eu web and OdourCollect App")
    args = argparser.parse_args()
    # argparser.print_help()
    # argparser.print_usage()
    if args.odourlist:
        from tabulate import tabulate
        cat_table = []
        for item in ochelpers.CATEGORY_LIST.items():
            cat_table.append([item[0], item[1]])
        print('Odour categories (to use in --category parameter:')
        print(tabulate(cat_table, headers=['Code', 'Category']))
        print()
        print('Odour types (to use in --type parameter:')
        type_table = []
        for item in ochelpers.TYPE_LIST.items():
            type_table.append([item[0], item[1].split('|')[0], item[1].split('|')[1]])
        print(tabulate(type_table, headers=['Code', 'Category', 'Odour Type']))
        exit(0)

    # Set some default query parameters
    # hedonic tone defaults (--hedonic=all)
    min_annoy = -4
    max_annoy = 4
    # Itensity filter defaults
    min_intensity = 0
    max_intensity = 6
    # type and subtype defaults. Called "category" and "type" in this tool.
    odour_type = 0
    odour_subtype = 0
    # dates
    date_init = datetime.date(2019, 1, 1)  # No observations before this date. OdourCollect was born in 2019
    date_end = datetime.date.today()
    # gps emission point of interest
    poi_coords = None
    # Now, (re)set some query parameters based on parsed args
    if args.hedonic == 'neutral':
        min_annoy = 0
        max_annoy = 0
    elif args.hedonic == 'pleasant':
        min_annoy = 1
        max_annoy = 4
    elif args.hedonic == 'unpleasant':
        min_annoy = -4
        max_annoy = -1
    if args.startdate:
        date_init = args.startdate
    if args.enddate:
        date_end = args.enddate
    if args.odourtype:  # subtype(OC) == type(pyOC). This is OK.
        odour_subtype = args.odourtype
    if args.category:
        odour_type = args.category
    if args.minintensity:
        min_intensity = args.minintensity
    if args.maxintensity:
        max_intensity = args.maxintensity
    if args.gps:
        add_point_of_interest = True
        poi_coords = ocmodels.GPScoords(lat=args.gps[0], long=args.gps[1])
    outputfile = args.output
    ochelpers.check_path(outputfile)
    # We are very explicit here. Some parameters are optional in OdourCollect's API but we always provide defaults
    requestparams = ocmodels.OCRequest(
        date_init=date_init,
        date_end=date_end,
        minAnnoy=min_annoy,
        maxAnnoy=max_annoy,
        minIntensity=min_intensity,
        maxIntensity=max_intensity,
        type=odour_type,
        subtype=odour_subtype
    )
    print('Making request to OdourCollect.eu API...')
    df = occore.get_oc_data(requestparams, outputfile, poi_coords)
    print('Saving obtained data to file: {}'.format(outputfile))
    ochelpers.df_to_file(df, outputfile)


if __name__ == "__main__":
    main()
