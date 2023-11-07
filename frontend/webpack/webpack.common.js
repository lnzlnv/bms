const path = require('path');
const webpack = require('webpack');

const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const { VueLoaderPlugin } = require("vue-loader");

module.exports = {
  entry: {
    main: './src/main.js',
    'toggle-navbar': './src/js/toggle-navbar.js',
    'player-stats-table': './src/vue//pages/stats/players/index.js',
    'team-stats-table': './src/vue/pages/stats/teams/index.js',
    'single-player-stats': './src/vue/pages/stats/single-player/index.js',
    'player-all-table': './src/vue/pages/players/all/index.js',
    'standings-table': './src/vue/pages/standings/all/index.js',
    'commissioner': './src/vue/pages/commissioner/commissioner/index.js',
    'commissioner-edit': './src/vue/pages/commissioner/edit/index.js',
    'admin-create-schedule': './src/vue/pages/admin/schedules/create/index.js',
    'admin-all-schedule': './src/vue/pages/admin/schedules/all/index.js',
    'admin-banner-schedule': './src/vue/pages/admin/schedules/banner/create/index.js',
    'admin-banner-all': './src/vue/pages/admin/schedules/banner/all/index.js',
    'admin-create-team': './src/vue/pages/admin/teams/create/index.js',
    'admin-all-team': './src/vue/pages/admin/teams/all/index.js',
    'admin-all-team-players': './src/vue/pages/admin/team-players/all/index.js',
    'admin-create-team-player': './src/vue/pages/admin/team-players/create/index.js',
    'admin-create-season': './src/vue/pages/admin/season/create/index.js',
    'admin-all-season': './src/vue/pages/admin/season/all/index.js',
    'admin-create-announcement': './src/vue/pages/admin/announcements/create/index.js',
    'admin-all-announcement': './src/vue/pages/admin/announcements/all/index.js',
    'admin-generate-account': './src/vue/pages/generate-account/generate/index.js',
    'admin-unupdated-accounts': './src/vue/pages/generate-account/unupdated/index.js',
    'admin-landing': './src/vue/pages/admin/landing/content/index.js',
    'admin-landing-add-image': './src/vue/pages/admin/landing/add-image/index.js',
    'admin-landing-add-highlights': './src/vue/pages/admin/landing/add-highlights/index.js',
    'admin-landing-add-news': './src/vue/pages/admin/landing/add-news/index.js',
    'statisticians-games-today': './src/vue/pages/statisticians/games-today/index.js',
    'statisticians-officiate-game': './src/vue/pages/statisticians/officiate-game/index.js',
    'stats-approval': './src/vue/pages/super_statistician/stats-approval/index.js',
    'stats-reports': './src/vue/pages/super_statistician/reports/index.js',
    'games-for-admin-approval':  './src/vue/pages/games-for-admin-approval/all/index.js',
    'games-admin-report': './src/vue/pages/games-for-admin-approval/report/index.js',
    'public-teams': './src/vue/pages/public/teams/index.js',
    'public-recaps': './src/vue/pages/public/recaps/index.js',
    'public-all-schedules': './src/vue/pages/public/all-schedules/index.js',
    'public-landing': './src/vue/pages/public/landing/index.js',
    'user-profile-update': './src/vue/pages/user_profile/update/index.js'
  },
  output: {
    path: path.resolve(__dirname,  '../public'),
    publicPath: '/',
    filename: '[name].js'
  },
  module: {
    rules: [
      {
        test:/\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader',
        ]
      },
      {
        test: /\.vue$/i,
        exclude: /(node_modules)/,
        use: {
          loader: "vue-loader",
        },
      },
      {
        test: /\.(js|jsx)$/,
        exclude: /(node_modules)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ["@babel/preset-env"],
          },
        }
      },
      {
        test: /\.html$/i,
        loader: "html-loader",
      },
      {
        test: /\.css$/i,
        use: [MiniCssExtractPlugin.loader, "css-loader", "style-loader"],
      },
      {
        test: /\.(?:ico|gif|png|jpg|jpeg|mp4)$/i,
        type: 'asset/resource',
      },
      {
        test: /\.(woff(2)?|eot|ttf|otf|svg|png|jpeg|mp4|webp)$/,
        type: 'asset/inline',
      },
    ]
  },
  plugins: [
    new VueLoaderPlugin(),
    new MiniCssExtractPlugin(),
    new webpack.DefinePlugin({
      __VUE_OPTIONS_API__: true,
      __VUE_PROD_DEVTOOLS__: false
    })
  ],
  resolve: {
    extensions: ['.js', '.jsx', '.scss', '.vue'],
    alias: {
      '@images': path.join(__dirname,  '../src/images/'),
      '@pages': path.join(__dirname,  '../src/vue/pages/'),
      '@composables': path.join(__dirname,  '../src/vue/composables/'),
      '@templates': path.join(__dirname, '../src/vue/templates/'),
      '@components': path.join(__dirname,  '../src/vue/components/'),
    },
  },
};